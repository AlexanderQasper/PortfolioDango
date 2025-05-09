from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import uuid
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=255, null=False, blank=False)
    email_verification_sent_at = models.DateTimeField(blank=True, null=True)
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
        from django.conf import settings
        from uuid import uuid4

        self.email_verification_token = uuid4().hex
        self.save()

        context = {
            'name': self.name,
            'token': self.email_verification_token
        }

        message = render_to_string('email/verification.html', context)

        send_mail(
            'Verify your email',
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            html_message=message
        )
