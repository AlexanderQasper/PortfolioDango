from django.contrib import admin
from .models import *

for model in [m for name, m in globals().items() if isinstance(m, type)]:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass