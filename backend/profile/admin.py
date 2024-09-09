from django.contrib import admin
from .models import Profile, StudentProfile, AdminProfile, LecturerProfile

admin.site.register(Profile)
admin.site.register(StudentProfile)
admin.site.register(AdminProfile)
admin.site.register(LecturerProfile)
