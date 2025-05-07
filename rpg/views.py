from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.contrib.auth import get_user_model
from .models import Achievement, Badge, UserProfile, UserAchievement, UserBadge
from .serializers import (
    AchievementSerializer, BadgeSerializer, UserProfileSerializer,
    UserAchievementSerializer, UserBadgeSerializer
)
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        # Try to get from cache first
        cache_key = f'user_profile_{self.request.user.id}'
        cached_profile = cache.get(cache_key)
        
        if cached_profile:
            return cached_profile
        
        # If not in cache, get from database
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        
        # Cache the profile for 5 minutes
        cache.set(cache_key, profile, 300)
        
        return profile

    @action(detail=False, methods=['get'])
    def achievements(self, request):
        profile = self.get_object()
        achievements = UserAchievement.objects.filter(user=request.user)
        serializer = UserAchievementSerializer(achievements, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def badges(self, request):
        profile = self.get_object()
        badges = UserBadge.objects.filter(user=request.user)
        serializer = UserBadgeSerializer(badges, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_xp(self, request):
        amount = request.data.get('amount', 0)
        if not isinstance(amount, int) or amount <= 0:
            return Response(
                {'error': 'Invalid XP amount'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profile = self.get_object()
        profile.add_xp(amount)
        
        # Invalidate cache
        cache.delete(f'user_profile_{request.user.id}')
        
        return Response(self.get_serializer(profile).data)
