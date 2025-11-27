from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentRegisterForm
from .forms import StudentRegisterForm, StudentUpdateForm
from .models import ContactMessage  # Import the model

# --- HOME PAGE ---
def home(request):
    return render(request, 'home.html')

# --- REGISTER ---
def register(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = StudentRegisterForm()
    
    return render(request, 'register.html', {'form': form})

# --- LOGIN ---
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

# --- LOGOUT ---
def logout_view(request):
    logout(request)
    return redirect('home')

# --- CONTACT US ---
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Save to Database
        ContactMessage.objects.create(name=name, email=email, message=message)
        
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
        
    return render(request, 'contact.html')
@login_required
def student_list(request):
    # 1. Get all students from the database
    students = User.objects.all()
    
    # 2. Send them to the template
    return render(request, 'student_list.html', {'students': students})
@login_required
def edit_student(request, id):
    # 1. Get the specific student by ID (or show 404 error)
    student = get_object_or_404(User, pk=id)
    
    if request.method == 'POST':
        # 2. Fill form with new data AND existing student instance
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student details updated successfully!')
            return redirect('student_list')
    else:
        # 3. Pre-fill form with current data
        form = StudentUpdateForm(instance=student)
    
    return render(request, 'edit_student.html', {'form': form})
@login_required
def delete_student(request, id):
    student = get_object_or_404(User, pk=id)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('student_list')
