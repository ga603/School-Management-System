import csv
import africastalking
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from .mpesa import lipa_na_mpesa

# Import Models
from .models import Student, ContactMessage, Attendance, LearningResource, StudentResult

# Import Forms
from .forms import StudentForm, StudentUpdateForm, ResourceForm, ResultForm

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
            return redirect('grade_dashboard') # Redirect to Dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# --- CONTACT US ---
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
    return render(request, 'contact.html')

# --- GRADE DASHBOARD (The Lobby) ---
@login_required
def grade_dashboard(request):
    grades = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8', 'Grade 9']
    return render(request, 'grade_dashboard.html', {'grades': grades})

# --- SPECIFIC GRADE LIST (The Classroom) ---
@login_required
def view_grade_students(request, grade_name):
    students = Student.objects.filter(grade_class=grade_name)
    return render(request, 'student_list.html', {'students': students, 'grade_name': grade_name})

# --- ADD STUDENT ---
@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('first_name')
            messages.success(request, f'Student {name} added successfully!')
            return redirect('grade_dashboard')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

# --- EDIT STUDENT ---
@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, pk=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student details updated successfully!')
            return redirect('view_grade_students', grade_name=student.grade_class)
    else:
        form = StudentForm(instance=student)
    return render(request, 'edit_student.html', {'form': form})

# --- DELETE STUDENT ---
@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, pk=id)
    grade = student.grade_class
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('view_grade_students', grade_name=grade)

# --- STUDENT LIST (With Search - Global) ---
@login_required
def student_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(admission_number__icontains=query)
        )
    else:
        students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

# --- MARK ATTENDANCE ---
@login_required
def mark_attendance(request, grade_name):
    students = Student.objects.filter(grade_class=grade_name)
    today = datetime.date.today()
    
    if request.method == 'POST':
        date = request.POST.get('date')
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            Attendance.objects.create(student=student, date=date, status=status)
        messages.success(request, f'Attendance marked for {grade_name} on {date}!')
        return redirect('grade_dashboard')

    return render(request, 'mark_attendance.html', {
        'students': students, 
        'grade_name': grade_name, 
        'today': str(today)
    })

# --- EXPORT ATTENDANCE TO CSV ---
@login_required
def export_attendance(request, grade_name):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{grade_name}_Attendance_Report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Student Name', 'Admission No', 'Status'])
    
    attendance_records = Attendance.objects.filter(student__grade_class=grade_name).order_by('-date')
    for record in attendance_records:
        writer.writerow([
            record.date, 
            f"{record.student.first_name} {record.student.last_name}",
            record.student.admission_number,
            record.status
        ])
    return response

# --- ASSIGNMENTS & RESOURCES ---
@login_required
def grade_resources(request, grade_name):
    resources = LearningResource.objects.filter(grade_class=grade_name).order_by('-uploaded_at')
    
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.grade_class = grade_name
            resource.save()
            messages.success(request, 'Assignment uploaded successfully!')
            return redirect('grade_resources', grade_name=grade_name)
    else:
        form = ResourceForm()

    return render(request, 'grade_resources.html', {
        'resources': resources,
        'grade_name': grade_name,
        'form': form
    })

# --- ADD EXAM RESULTS ---
@login_required
def add_result(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.student = student
            result.save()
            messages.success(request, f'Result added for {student.first_name}!')
            return redirect('add_result', student_id=student.id)
    else:
        form = ResultForm()
    
    return render(request, 'add_result.html', {'form': form, 'student': student})

# --- VIEW REPORT CARD ---
@login_required
def student_report(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    results = StudentResult.objects.filter(student=student).order_by('exam', 'subject')
    
    return render(request, 'student_report.html', {
        'student': student, 
        'results': results
    })
# --- PUBLIC PARENT PORTAL ---
def parent_portal(request):
    student = None
    assignments = None
    results = None
    error = None

    if 'admission_number' in request.GET:
        adm_no = request.GET.get('admission_number')
        try:
            # Try to find the student
            student = Student.objects.get(admission_number=adm_no)
            
            # If found, get their assignments (based on Grade)
            assignments = LearningResource.objects.filter(grade_class=student.grade_class).order_by('-uploaded_at')
            
            # Get their exam results
            results = StudentResult.objects.filter(student=student).order_by('exam', 'subject')
            
        except Student.DoesNotExist:
            error = "Student not found. Please check the Admission Number."

    return render(request, 'parent_portal.html', {
        'student': student,
        'assignments': assignments,
        'results': results,
        'error': error
    })
# --- SEND SMS ---
@login_required
def send_sms(request):
    grades = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8', 'Grade 9']
    
    if request.method == 'POST':
        selected_grade = request.POST.get('grade')
        message_content = request.POST.get('message')
        
        # 1. Get parents' phone numbers for that grade
        students = Student.objects.filter(grade_class=selected_grade)
        phone_numbers = []
        
        for student in students:
            phone = student.parent_contact
            # Fix format: 0722... -> +254722...
            if phone.startswith('0'):
                phone = '+254' + phone[1:]
            phone_numbers.append(phone)
            
        # 2. Send SMS using Africa's Talking (Sandbox Mode)
        if phone_numbers:
            # TODO: Replace these with your REAL credentials when you deploy!
            username = "sandbox" 
            api_key = "atsk_..." # You will get this from the dashboard later
            
            # Initialize the SDK
            try:
                africastalking.initialize(username, api_key)
                sms = africastalking.SMS
                
                # Send the message
                # Note: In sandbox, you can only send to verified numbers.
                # For now, we simulate success so the app doesn't crash.
                print(f"SENDING SMS TO: {phone_numbers}") # Print to terminal to prove logic works
                
                messages.success(request, f"Message queued for {len(phone_numbers)} parents in {selected_grade}!")
            except Exception as e:
                messages.error(request, f"SMS Error: {str(e)}")
        else:
            messages.warning(request, "No students found in that grade with contact numbers.")
            
        return redirect('send_sms')

    return render(request, 'send_sms.html', {'grades': grades})

def pay_fees(request):
    if request.method == 'POST':
        adm_no = request.POST.get('admission_number')
        phone = request.POST.get('phone')
        amount = 1 # Keep 1 KES for testing

        try:
            # 1. Verify the Student exists
            student = Student.objects.get(admission_number=adm_no)
            
            # 2. Trigger M-Pesa
            response = lipa_na_mpesa(phone, amount, account_ref=f"Fee-{adm_no}")
            
            # 3. Check M-Pesa Response
            if response.get('ResponseCode') == '0':
                messages.success(request, f"Payment initiated for {student.first_name}. Check phone to enter PIN!")
            else:
                error_message = response.get('errorMessage', 'Unknown error')
                messages.error(request, f"Payment failed: {error_message}")
                
        except Student.DoesNotExist:
            messages.error(request, f"Student with Admission Number {adm_no} not found.")
            
        return redirect('pay_fees')
        
    return render(request, 'pay_fees.html')

@login_required
def promote_students(request):
    if request.method == 'POST':
        # Logic: Grade 1 -> Grade 2, etc.
        grade_order = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8', 'Grade 9']
        
        count = 0
        # We go backwards (Grade 8 -> 9) so we don't double-promote someone
        for i in range(len(grade_order) - 2, -1, -1): 
            current_grade = grade_order[i]
            next_grade = grade_order[i+1]
            
            # Find students in current grade and move them
            students = Student.objects.filter(grade_class=current_grade)
            for s in students:
                s.grade_class = next_grade
                s.save()
                count += 1
                
        # Handle Grade 9 (Graduating?) - Optional logic here
        
        messages.success(request, f"Successfully promoted {count} students to the next grade!")
        return redirect('grade_dashboard')

    return render(request, 'promote_confirm.html')
