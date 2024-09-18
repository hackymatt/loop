from django.contrib import admin
from .models import Schedule, Meeting, Recording

admin.site.register(Schedule)
admin.site.register(Meeting)
admin.site.register(Recording)
