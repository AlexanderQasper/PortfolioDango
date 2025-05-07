from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import File, Notification
from .utils import validate_file_type, validate_file_size, get_file_category

@shared_task
def process_uploaded_file(file_id):
    """Process uploaded file in the background."""
    try:
        file = File.objects.get(id=file_id)
        
        # Validate file
        validate_file_type(file.file)
        validate_file_size(file.file)
        
        # Set file category
        file.category = get_file_category(file.file)
        file.save()
        
        # Create notification
        Notification.objects.create(
            user=file.owner,
            message=f'File {file.name} has been processed successfully.',
            type='success'
        )
        
        return f'File {file.name} processed successfully'
    except Exception as e:
        # Create error notification
        Notification.objects.create(
            user=file.owner,
            message=f'Error processing file {file.name}: {str(e)}',
            type='error'
        )
        raise

@shared_task
def send_email_notification(user_id, subject, message):
    """Send email notification in the background."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    try:
        user = User.objects.get(id=user_id)
        html_message = render_to_string('email/notification.html', {
            'user': user,
            'message': message
        })
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return f'Email sent to {user.email}'
    except Exception as e:
        raise

@shared_task
def cleanup_old_files():
    """Clean up old files that are no longer needed."""
    from django.utils import timezone
    from datetime import timedelta
    
    # Delete files older than 30 days
    old_files = File.objects.filter(
        created_at__lt=timezone.now() - timedelta(days=30),
        is_deleted=True
    )
    
    count = old_files.count()
    old_files.delete()
    
    return f'Deleted {count} old files' 