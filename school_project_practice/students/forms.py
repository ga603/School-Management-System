from django import forms
from .models import Student, LearningResource, StudentResult, ReportComment

# --- STUDENT FORM (Removed 'email') ---
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'admission_number', 'grade_class', 'parent_contact', 'passport_photo']

# --- RESOURCE FORM (For Assignments/Videos) ---
class ResourceForm(forms.ModelForm):
    class Meta:
        model = LearningResource
        fields = ['title', 'resource_type', 'file', 'video_link']
        widgets = {
            'video_link': forms.URLInput(attrs={'placeholder': 'https://youtube.com/...'}),
        }

# --- RESULT FORM (For Marks) ---
class ResultForm(forms.ModelForm):
    class Meta:
        model = StudentResult
        fields = ['subject', 'exam_type', 'exam_name', 'performance_level']
        widgets = {
            'exam_name': forms.TextInput(attrs={'placeholder': 'e.g. Term 1 2025'}),
        }

# --- COMMENT FORM (For Teachers) ---
class CommentForm(forms.ModelForm):
    class Meta:
        model = ReportComment
        fields = ['exam_name', 'teacher_comment']
        widgets = {
            'teacher_comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Class Teacher Remarks...'}),
            'exam_name': forms.TextInput(attrs={'placeholder': 'e.g. Term 1 2025'}),
        }