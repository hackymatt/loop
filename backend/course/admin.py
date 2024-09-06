from django.contrib import admin
from .models import Course

admin.site.register(Course)
admin.site.register(Course.modules.through)
admin.site.register(Course.skills.through)
admin.site.register(Course.topics.through)
