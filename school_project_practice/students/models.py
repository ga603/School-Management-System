from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True) # Automatically records time

    def __str__(self):
        return f"Message from {self.name}"
    
class Student(models.Model):
    admission_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True) # Optional for kids
    parent_contact = models.CharField(max_length=15) # New Field!
    grade_class = models.CharField(max_length=20) # e.g., "Grade 4"
    passport_photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"