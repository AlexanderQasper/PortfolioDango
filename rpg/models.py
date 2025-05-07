from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils import timezone

User = get_user_model()

class CharacterClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_xp = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Achievement(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'))
    icon = models.ImageField(_('icon'), upload_to='achievements/', null=True, blank=True)
    xp_reward = models.IntegerField(_('XP reward'), validators=[MinValueValidator(0)])
    is_hidden = models.BooleanField(_('is hidden'), default=False)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    class Meta:
        verbose_name = _('achievement')
        verbose_name_plural = _('achievements')
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['xp_reward']),
        ]

    def __str__(self):
        return self.name

class Badge(models.Model):
    name = models.CharField(_('name'), max_length=100, unique=True)
    description = models.TextField(_('description'))
    icon = models.ImageField(_('icon'), upload_to='badges/', null=True, blank=True)
    rarity = models.CharField(_('rarity'), max_length=20, choices=[
        ('common', 'Common'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
    ])
    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    class Meta:
        verbose_name = _('badge')
        verbose_name_plural = _('badges')
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['rarity']),
        ]

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rpg_profile')
    character_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True)
    xp = models.IntegerField(_('XP'), default=0, validators=[MinValueValidator(0)])
    level = models.IntegerField(_('level'), default=1, validators=[MinValueValidator(1)])
    achievements = models.ManyToManyField(Achievement, through='UserAchievement', related_name='users')
    badges = models.ManyToManyField(Badge, through='UserBadge', related_name='users')
    last_activity = models.DateTimeField(_('last activity'), auto_now=True)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        indexes = [
            models.Index(fields=['xp']),
            models.Index(fields=['level']),
            models.Index(fields=['last_activity']),
        ]

    def __str__(self):
        return f"{self.user.email}'s RPG Profile"

    @property
    def next_level_xp(self):
        # Example level progression: 1000 XP per level
        return (self.level * 1000)

    def add_xp(self, amount):
        self.xp += amount
        while self.xp >= self.next_level_xp:
            self.level_up()
        self.save()

    def level_up(self):
        self.level += 1
        # Trigger any level-up events here

class UserAchievement(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(_('unlocked at'), auto_now_add=True)
    progress = models.IntegerField(_('progress'), default=0)
    is_completed = models.BooleanField(_('is completed'), default=False)

    class Meta:
        unique_together = ['user_profile', 'achievement']
        indexes = [
            models.Index(fields=['user_profile', 'achievement']),
            models.Index(fields=['is_completed']),
        ]

    def __str__(self):
        return f"{self.user_profile.user.email} - {self.achievement.name}"

class UserBadge(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(_('awarded at'), auto_now_add=True)

    class Meta:
        unique_together = ['user_profile', 'badge']
        indexes = [
            models.Index(fields=['user_profile', 'badge']),
        ]

    def __str__(self):
        return f"{self.user_profile.user.email} - {self.badge.name}"
