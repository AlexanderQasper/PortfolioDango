from django.contrib import admin
from axes.models import AccessAttempt, AccessLog
from .models import User

admin.site.register(User)

try:
    admin.site.register(AccessAttempt)
except admin.sites.AlreadyRegistered:
    pass

try:
    admin.site.register(AccessLog)
except admin.sites.AlreadyRegistered:
    pass