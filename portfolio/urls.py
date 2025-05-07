from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TrackViewSet, CategoryViewSet, FolderViewSet,
    CustomCriteriaViewSet, FileViewSet, NotificationViewSet
)

router = DefaultRouter()
router.register(r'tracks', TrackViewSet, basename='track')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'folders', FolderViewSet, basename='folder')
router.register(r'criteria', CustomCriteriaViewSet, basename='criteria')
router.register(r'files', FileViewSet, basename='file')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
] 