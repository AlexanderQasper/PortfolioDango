from django.contrib import admin
from . import models
from django.db import models as django_models

for name in dir(models):
    obj = getattr(models, name)
    if isinstance(obj, type) and issubclass(obj, django_models.Model):
        try:
            admin.site.register(obj)
        except admin.sites.AlreadyRegistered:
            pass