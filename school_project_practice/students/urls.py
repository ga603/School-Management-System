from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # Student Management
    path('add/', views.add_student, name='add_student'),
    path('students/', views.student_list, name='student_list'),
    path('edit/<int:id>/', views.edit_student, name='edit_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    
    # Grade & Dashboard
    path('dashboard/', views.grade_dashboard, name='grade_dashboard'),
    path('grade/<str:grade_name>/', views.view_grade_students, name='view_grade_students'),
    
    # Features
    path('grade/<str:grade_name>/attendance/', views.mark_attendance, name='mark_attendance'),
    path('grade/<str:grade_name>/resources/', views.grade_resources, name='grade_resources'),
    path('grade/<str:grade_name>/export_attendance/', views.export_attendance, name='export_attendance'),
    
    # Exams & Results
    path('student/<int:student_id>/add_result/', views.add_result, name='add_result'),
    
    # --- THIS WAS MISSING ---
    path('student/<int:student_id>/report/', views.student_report, name='student_report'),
    path('portal/', views.parent_portal, name='parent_portal'),
    path('sms/', views.send_sms, name='send_sms'),
    path('pay/', views.pay_fees, name='pay_fees'),
    path('promote/', views.promote_students, name='promote_students'),
]