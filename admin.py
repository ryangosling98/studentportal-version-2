
# Register your models here.
from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'major', 'gpa')
    search_fields = ('user__username', 'student_id', 'major')
