from django.contrib import admin
from .models import Student, Attendance, Subject, StudentResult, LearningResource, ContactMessage, ReportComment

# Register your models here
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(Subject)
admin.site.register(StudentResult)
admin.site.register(LearningResource)
admin.site.register(ContactMessage)
admin.site.register(ReportComment)  # <--- Register the new Comments model