from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Student, ContactMessage
from .forms import StudentForm

# --- HOME PAGE ---
def home(request):
    return render(request, 'home.html')

# --- AUTHENTICATION (Login/Logout) ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# --- ADD STUDENT (With Image Handling) ---
@login_required
def add_student(request):
    if request.method == 'POST':
        # CRITICAL UPDATE: Added request.FILES here to catch the photo
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('first_name')
            messages.success(request, f'Student {name} added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

# --- STUDENT LIST (With Search) ---
@login_required
def student_list(request):
    query = request.GET.get('q') # Get search term
    
    if query:
        # Search by First Name OR Last Name OR Admission Number
        students = Student.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(admission_number__icontains=query)
        )
    else:
        students = Student.objects.all()
    
    return render(request, 'student_list.html', {'students': students})

# --- EDIT STUDENT (With Image Handling) ---
@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, pk=id)
    
    if request.method == 'POST':
        # CRITICAL UPDATE: Added request.FILES here to update the photo
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student details updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'edit_student.html', {'form': form})

# --- DELETE STUDENT ---
@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, pk=id)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('student_list')

# --- CONTACT US ---
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Save message to database
        ContactMessage.objects.create(name=name, email=email, message=message)
        
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
        
    return render(request, 'contact.html')