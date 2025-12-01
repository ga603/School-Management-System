from django import forms
from .models import Student, LearningResource, StudentResult

# Form for Adding a New Student
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['admission_number', 'first_name', 'last_name', 'grade_class', 'parent_contact', 'email', 'passport_photo']

# Form for Editing an Existing Student
# We update the model to 'Student' and remove 'username'
class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['admission_number', 'first_name', 'last_name', 'grade_class', 'parent_contact', 'email', 'passport_photo']

# Form for Uploading Assignments
class ResourceForm(forms.ModelForm):
    class Meta:
        model = LearningResource
        fields = ['title', 'file',]
class ResultForm(forms.ModelForm):
    class Meta:
        model = StudentResult
        # Changed 'score' to 'performance_level'
        fields = ['exam', 'subject', 'performance_level'] 
        widgets = {
            # This makes it a nice dropdown menu
            'performance_level': forms.Select(attrs={'class': 'form-select'}),
        }