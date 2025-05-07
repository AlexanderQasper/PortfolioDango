from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Track, Category, Folder, CustomCriteria, File, Notification

User = get_user_model()

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'name', 'description', 'icon', 'created_at']
        read_only_fields = ['id', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        user = self.context['request'].user
        if Category.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'description', 'parent', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        name = data.get('name')
        parent = data.get('parent')

        if Folder.objects.filter(user=user, name=name, parent=parent).exists():
            raise serializers.ValidationError("A folder with this name already exists in this location.")
        
        if parent and parent.user != user:
            raise serializers.ValidationError("Cannot create folder in another user's folder.")
        
        return data

class CustomCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomCriteria
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        user = self.context['request'].user
        if CustomCriteria.objects.filter(user=user, name=value).exists():
            raise serializers.ValidationError("A criteria with this name already exists.")
        return value

class FileSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    custom_criteria = CustomCriteriaSerializer(many=True, read_only=True)
    category_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    criteria_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = File
        fields = [
            'id', 'title', 'description', 'file', 'folder', 'categories',
            'custom_criteria', 'track', 'is_public', 'uploaded_at', 'updated_at',
            'category_ids', 'criteria_ids'
        ]
        read_only_fields = ['id', 'uploaded_at', 'updated_at']

    def validate(self, data):
        user = self.context['request'].user
        folder = data.get('folder')
        
        if folder and folder.user != user:
            raise serializers.ValidationError("Cannot add file to another user's folder.")
        
        return data

    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        criteria_ids = validated_data.pop('criteria_ids', [])
        
        file = File.objects.create(**validated_data)
        
        # Add categories and criteria
        if category_ids:
            categories = Category.objects.filter(id__in=category_ids, user=file.user)
            file.categories.set(categories)
        
        if criteria_ids:
            criteria = CustomCriteria.objects.filter(id__in=criteria_ids, user=file.user)
            file.custom_criteria.set(criteria)
        
        return file 

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'type', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def update(self, instance, validated_data):
        if 'is_read' in validated_data:
            instance.mark_as_read()
        return instance 