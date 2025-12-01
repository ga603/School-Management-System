from django.contrib import admin
from .models import ContactMessage, Student, LearningResource, Attendance, Subject, Exam, StudentResult

# Register your models here.
admin.site.register(ContactMessage)
admin.site.register(Student)
admin.site.register(LearningResource)
admin.site.register(Attendance)

# New Exam Modules
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(StudentResult)