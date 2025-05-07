from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    is_email_verified = models.BooleanField(_('email verified'), default=False)
    email_verification_token = models.UUIDField(_('email verification token'), default=uuid.uuid4, editable=False)
    email_verification_sent_at = models.DateTimeField(_('verification sent at'), null=True, blank=True)
    name = models.CharField(_('full name'), max_length=255)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(_('bio'), blank=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']
    
    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['is_email_verified']),
        ]
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email

    def send_verification_email(self):
        """Send email verification link."""
        from django.template.loader import render_to_string
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        
        subject = _('Verify your email address')
        context = {
            'user': self,
            'verification_url': f"{settings.FRONTEND_URL}/verify-email/{self.email_verification_token}/"
        }
        message = render_to_string('email/verification.html', context)
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.email],
            html_message=message,
            fail_silently=False,
        )
        
        self.email_verification_sent_at = timezone.now()
        self.save()
