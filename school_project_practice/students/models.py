from django.db import models
GRADE_CHOICES = [
    ('Grade 1', 'Grade 1'),
    ('Grade 2', 'Grade 2'),
    ('Grade 3', 'Grade 3'),
    ('Grade 4', 'Grade 4'),
    ('Grade 5', 'Grade 5'),
    ('Grade 6', 'Grade 6'),
    ('Grade 7', 'Grade 7'),
    ('Grade 8', 'Grade 8'),
    ('Grade 9', 'Grade 9'),
]

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
    grade_class = models.CharField(max_length=20, choices=GRADE_CHOICES)
    passport_photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')

    def __str__(self):
        return f"{self.student.first_name} - {self.date} - {self.status}"
class LearningResource(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='assignments/') # Stores PDFs, Word docs, etc.
    grade_class = models.CharField(max_length=20, choices=GRADE_CHOICES) # Links to Grade 1-9
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.grade_class})"
# 1. Subjects (Math, English, Kiswahili...)
class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# 2. Exams (Term 1, Term 2, Opener...)
class Exam(models.Model):
    name = models.CharField(max_length=100) # e.g., "Term 1 2025"
    start_date = models.DateField()

    def __str__(self):
        return self.name

# 3. Results (The actual marks)
class StudentResult(models.Model):
    # [cite_start]CBC Grading Scale (1-7) [cite: 1]
    PERFORMANCE_LEVELS = [
        (7, '7 - Exceeding Expectations'),
        (6, '6 - Above Expectations'),
        (5, '5 - Meeting Expectations'),
        (4, '4 - Approaching Expectations'),
        (3, '3 - Below Expectations'),
        (2, '2 - Emerging'),
        (1, '1 - Needs Support'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    # Changed from 'score' to 'performance_level'
    performance_level = models.IntegerField(choices=PERFORMANCE_LEVELS, default=4)
    
    # Optional: Keep score if they still do written tests, otherwise remove it
    # score = models.IntegerField(null=True, blank=True) 

    # [cite_start]Logic to automatically get the Interpretation text [cite: 1]
    @property
    def interpretation(self):
        interpretations = {
            7: "Demonstrates exceptional mastery and applies knowledge in new situations.",
            6: "Performs tasks with minimal guidance and shows deep understanding.",
            5: "Meets the expected level of competency independently.",
            4: "Shows progress but requires some support to meet expectations.",
            3: "Beginning to grasp concepts but needs significant support.",
            2: "Shows minimal understanding; requires close guidance.",
            1: "Has major difficulties understanding and applying concepts."
        }
        return interpretations.get(self.performance_level, "")

    @property
    def short_grade(self):
        # Helper for the Table view (EE, AE, ME...)
        mapping = {
            7: "EE", 6: "AE", 5: "ME", 4: "ApE", 3: "BE", 2: "Em", 1: "NS"
        }
        return mapping.get(self.performance_level, "")

    def __str__(self):
        return f"{self.student} - {self.subject}: Level {self.performance_level}"