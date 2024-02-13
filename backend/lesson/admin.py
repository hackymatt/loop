from django.contrib import admin
from .models import Lesson, LessonPriceHistory, Technology

admin.site.register(Lesson)
admin.site.register(LessonPriceHistory)
admin.site.register(Technology)
