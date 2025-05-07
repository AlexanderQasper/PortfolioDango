from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UniversityViewSet, TemplateViewSet

router = DefaultRouter()
router.register(r'universities', UniversityViewSet)
router.register(r'templates', TemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 