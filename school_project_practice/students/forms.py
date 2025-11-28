from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django import forms
from .models import Student # Import the new model

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['admission_number', 'first_name', 'last_name', 'grade_class', 'parent_contact', 'email', 'passport_photo']


class StudentUpdateForm(forms.ModelForm):
  
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']