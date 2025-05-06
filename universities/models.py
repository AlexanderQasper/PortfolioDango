from django.db import models

# Create your models here.

class University(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='university_logos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Template(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='templates')
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='university_templates/')
    requirements = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.university.name}"
