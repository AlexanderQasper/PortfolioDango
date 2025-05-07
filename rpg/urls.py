from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AchievementViewSet, BadgeViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'badges', BadgeViewSet, basename='badge')
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
] 