from django.shortcuts import render
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserSerializer
from .permissions import IsSelfOrAdmin
from django.utils import timezone

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class UserLoginView(TokenObtainPairView):
    pass

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['post'])
    def verify_email(self, request):
        """Verify email using token."""
        token = request.data.get('token')
        if not token:
            return Response(
                {'error': 'Token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(email_verification_token=token)
            if user.is_email_verified:
                return Response(
                    {'error': 'Email already verified'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.is_email_verified = True
            user.save()
            return Response({'status': 'Email verified successfully'})
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid token'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def resend_verification(self, request):
        """Resend verification email."""
        user = request.user
        if user.is_email_verified:
            return Response(
                {'error': 'Email already verified'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if we can resend (e.g., not too frequent)
        if user.email_verification_sent_at:
            time_since_last = timezone.now() - user.email_verification_sent_at
            if time_since_last.total_seconds() < 300:  # 5 minutes
                return Response(
                    {'error': 'Please wait before requesting another verification email'},
                    status=status.HTTP_429_TOO_MANY_REQUESTS
                )
        
        user.send_verification_email()
        return Response({'status': 'Verification email sent'})
