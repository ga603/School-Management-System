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
    
    # Student Management (The new names)
    path('add/', views.add_student, name='add_student'), # Points to views.add_student
    path('students/', views.student_list, name='student_list'),
    path('edit/<int:id>/', views.edit_student, name='edit_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
]