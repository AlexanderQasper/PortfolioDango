from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='portfolio_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.title} - {self.user.email}"
