from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import File, Notification
from .tasks import process_uploaded_file
from django.core.files.uploadedfile import SimpleUploadedFile
import os

User = get_user_model()

class NotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Create test notification
        self.notification = Notification.objects.create(
            user=self.user,
            message='Test notification',
            type='info'
        )
    
    def test_get_notifications(self):
        """Test retrieving user notifications."""
        response = self.client.get('/api/portfolio/notifications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message'], 'Test notification')
    
    def test_mark_notification_read(self):
        """Test marking a notification as read."""
        response = self.client.patch(
            f'/api/portfolio/notifications/{self.notification.id}/',
            {'is_read': True}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
    
    def test_mark_all_read(self):
        """Test marking all notifications as read."""
        # Create another notification
        Notification.objects.create(
            user=self.user,
            message='Another test notification',
            type='info'
        )
        
        response = self.client.post('/api/portfolio/notifications/mark_all_read/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        unread_count = Notification.objects.filter(
            user=self.user,
            is_read=False
        ).count()
        self.assertEqual(unread_count, 0)
    
    def test_unread_count(self):
        """Test getting unread notification count."""
        response = self.client.get('/api/portfolio/notifications/unread_count/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['unread_count'], 1)

class FileProcessingTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test file
        self.test_file = SimpleUploadedFile(
            name='test.txt',
            content=b'Test file content',
            content_type='text/plain'
        )
        
        self.file = File.objects.create(
            name='test.txt',
            file=self.test_file,
            owner=self.user
        )
    
    def test_file_processing(self):
        """Test file processing task."""
        result = process_uploaded_file.delay(self.file.id)
        result.get()  # Wait for task to complete
        
        self.file.refresh_from_db()
        self.assertEqual(self.file.category, 'document')
        
        # Check if notification was created
        notification = Notification.objects.filter(
            user=self.user,
            message__contains='processed successfully'
        ).first()
        self.assertIsNotNone(notification)
    
    def test_invalid_file_type(self):
        """Test processing invalid file type."""
        invalid_file = SimpleUploadedFile(
            name='test.exe',
            content=b'Invalid file content',
            content_type='application/x-msdownload'
        )
        
        file = File.objects.create(
            name='test.exe',
            file=invalid_file,
            owner=self.user
        )
        
        with self.assertRaises(Exception):
            process_uploaded_file.delay(file.id).get()
        
        # Check if error notification was created
        notification = Notification.objects.filter(
            user=self.user,
            type='error'
        ).first()
        self.assertIsNotNone(notification)
