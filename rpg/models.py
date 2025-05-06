from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CharacterClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_xp = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    xp_reward = models.IntegerField()
    icon = models.ImageField(upload_to='achievements/', null=True, blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rpg_profile')
    character_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    achievements = models.ManyToManyField(Achievement, blank=True)

    def __str__(self):
        return f"{self.user.email}'s RPG Profile"
