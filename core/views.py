from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail
import redis
import psutil
import os

def index(request):
    return JsonResponse({"message": "API is running"})

class HealthCheckView(APIView):
    permission_classes = []  # No authentication required
    
    def get(self, request):
        """Check system health status."""
        health_status = {
            'status': 'healthy',
            'components': {}
        }
        
        # Check database
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            health_status['components']['database'] = 'healthy'
        except Exception as e:
            health_status['components']['database'] = f'error: {str(e)}'
            health_status['status'] = 'unhealthy'
        
        # Check Redis cache
        try:
            cache.set('health_check', 'ok', 1)
            if cache.get('health_check') == 'ok':
                health_status['components']['cache'] = 'healthy'
            else:
                health_status['components']['cache'] = 'error: cache not working'
                health_status['status'] = 'unhealthy'
        except Exception as e:
            health_status['components']['cache'] = f'error: {str(e)}'
            health_status['status'] = 'unhealthy'
        
        # Check system resources
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            health_status['components']['system'] = {
                'cpu_usage': f'{cpu_percent}%',
                'memory_usage': f'{memory.percent}%',
                'disk_usage': f'{disk.percent}%',
                'status': 'healthy' if all([
                    cpu_percent < 90,
                    memory.percent < 90,
                    disk.percent < 90
                ]) else 'warning'
            }
            
            if health_status['components']['system']['status'] == 'warning':
                health_status['status'] = 'warning'
        except Exception as e:
            health_status['components']['system'] = f'error: {str(e)}'
            health_status['status'] = 'unhealthy'
        
        return Response(health_status)


class SendEmailView(APIView):
    permission_classes = []

    def post(self, request):
        from django.core.mail import send_mail
        from django.conf import settings

        data = request.data
        subject = data.get("subject", "Test Subject")
        message = data.get("message", "Test message body.")
        recipient = data.get("recipient", settings.EMAIL_HOST_USER)

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient],
                fail_silently=False,
            )
            return Response({'status': 'Email sent successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)