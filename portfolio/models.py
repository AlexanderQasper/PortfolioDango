from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Track(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'))
    icon = models.CharField(_('icon'), max_length=50, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('track')
        verbose_name_plural = _('tracks')
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        unique_together = ['name', 'user']
        indexes = [
            models.Index(fields=['name', 'user']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.user.email})"

class Folder(models.Model):
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='folders')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('folder')
        verbose_name_plural = _('folders')
        unique_together = ['name', 'user', 'parent']
        indexes = [
            models.Index(fields=['name', 'user']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.user.email})"

class CustomCriteria(models.Model):
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_criteria')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('custom criteria')
        verbose_name_plural = _('custom criteria')
        unique_together = ['name', 'user']
        indexes = [
            models.Index(fields=['name', 'user']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.user.email})"

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    file = models.FileField(_('file'), upload_to='portfolio_files/')
    folder = models.ForeignKey(Folder, on_delete=models.SET_NULL, null=True, blank=True, related_name='files')
    categories = models.ManyToManyField(Category, related_name='files', blank=True)
    custom_criteria = models.ManyToManyField(CustomCriteria, related_name='files', blank=True)
    track = models.ForeignKey(Track, on_delete=models.SET_NULL, null=True, blank=True, related_name='files')
    is_public = models.BooleanField(_('is public'), default=False)
    uploaded_at = models.DateTimeField(_('uploaded at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')
        indexes = [
            models.Index(fields=['user', 'title']),
            models.Index(fields=['user', 'uploaded_at']),
            models.Index(fields=['is_public']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.user.email})"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('success', _('Success')),
        ('error', _('Error')),
        ('info', _('Info')),
        ('warning', _('Warning')),
    )
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('user')
    )
    message = models.TextField(verbose_name=_('message'))
    type = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPES,
        default='info',
        verbose_name=_('type')
    )
    is_read = models.BooleanField(default=False, verbose_name=_('is read'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    
    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f'{self.user.username} - {self.message[:50]}'
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
