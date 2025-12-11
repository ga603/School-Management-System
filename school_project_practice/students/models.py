from django.db import models
from django.contrib.auth.models import User

# --- 1. STUDENT MODEL ---
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    admission_number = models.CharField(max_length=20, unique=True)
    grade_class = models.CharField(max_length=20, choices=[
        ('Grade 1', 'Grade 1'), ('Grade 2', 'Grade 2'), ('Grade 3', 'Grade 3'),
        ('Grade 4', 'Grade 4'), ('Grade 5', 'Grade 5'), ('Grade 6', 'Grade 6'),
        ('Grade 7', 'Grade 7'), ('Grade 8', 'Grade 8'), ('Grade 9', 'Grade 9'),
    ])
    parent_contact = models.CharField(max_length=15)
    passport_photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.admission_number})"

# --- 2. ATTENDANCE MODEL ---
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late')
    ])

    def __str__(self):
        return f"{self.student.first_name} - {self.date} - {self.status}"

# --- 3. SUBJECT MODEL ---
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

# --- 4. EXAM RESULT MODEL (Updated) ---
class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # New: Exam Type Selection
    exam_type = models.CharField(max_length=20, choices=[
        ('Opener', 'Opener Exam'),
        ('Midterm', 'Midterm Exam'),
        ('Endterm', 'End of Term Exam'),
    ], default='Midterm')
    exam_name = models.CharField(max_length=100) # e.g., "Term 1 2025"
    performance_level = models.IntegerField(choices=[(i, str(i)) for i in range(1, 8)])
    
    @property
    def short_grade(self):
        grades = {1: 'BE', 2: 'BE', 3: 'ApE', 4: 'ApE', 5: 'ME', 6: 'AE', 7: 'EE'}
        return grades.get(self.performance_level, '-')

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.exam_type}"

# --- 5. NEW: TEACHER COMMENT MODEL ---
class ReportComment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100) # e.g. "Term 1 2025"
    teacher_comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment for {self.student} - {self.exam_name}"

# --- 6. LEARNING RESOURCES (Updated for Videos & Newsletters) ---
class LearningResource(models.Model):
    title = models.CharField(max_length=200)
    grade_class = models.CharField(max_length=20)
    
    # New: Resource Type
    resource_type = models.CharField(max_length=20, choices=[
        ('Assignment', 'Assignment/Notes'),
        ('Video', 'Video Link'),
        ('Newsletter', 'School Communication'),
    ], default='Assignment')
    
    # Files are for assignments/newsletters
    file = models.FileField(upload_to='resources/', blank=True, null=True)
    
    # Links are for YouTube/Videos
    video_link = models.URLField(blank=True, null=True, help_text="Paste YouTube link here")
    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.resource_type})"

# --- 7. CONTACT MESSAGE ---
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.name}"