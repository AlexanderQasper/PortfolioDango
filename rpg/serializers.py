from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Achievement, Badge, UserProfile, UserAchievement, UserBadge

User = get_user_model()

class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'icon', 'xp_reward', 'is_hidden', 'created_at']
        read_only_fields = ['id', 'created_at']

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ['id', 'name', 'description', 'icon', 'rarity', 'created_at']
        read_only_fields = ['id', 'created_at']

class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)
    
    class Meta:
        model = UserAchievement
        fields = ['achievement', 'progress', 'is_completed', 'unlocked_at']
        read_only_fields = ['unlocked_at']

class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = UserBadge
        fields = ['badge', 'awarded_at']
        read_only_fields = ['awarded_at']

class UserProfileSerializer(serializers.ModelSerializer):
    achievements = UserAchievementSerializer(source='userachievement_set', many=True, read_only=True)
    badges = UserBadgeSerializer(source='userbadge_set', many=True, read_only=True)
    next_level_xp = serializers.SerializerMethodField()
    progress_to_next_level = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'xp', 'level', 'achievements', 'badges', 'last_activity',
            'next_level_xp', 'progress_to_next_level'
        ]
        read_only_fields = ['xp', 'level', 'last_activity']

    def get_next_level_xp(self, obj):
        return obj.next_level_xp

    def get_progress_to_next_level(self, obj):
        if obj.level == 1:
            return obj.xp / 1000 * 100
        return (obj.xp % 1000) / 1000 * 100 