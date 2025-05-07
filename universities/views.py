from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import University, Template
from rest_framework import serializers

# Create your views here.

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name', 'description', 'logo']

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'university', 'name', 'description', 'file', 'requirements']

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Template.objects.all()
        university_id = self.request.query_params.get('university', None)
        if university_id is not None:
            queryset = queryset.filter(university_id=university_id)
        return queryset
