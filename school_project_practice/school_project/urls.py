from django.contrib import admin  # <--- Import must come first
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from students import views

# --- REBRANDING GOES HERE (After imports) ---
admin.site.site_header = "ElimuTrack Admin"
admin.site.site_title = "ElimuTrack Portal"
admin.site.index_title = "Welcome to ElimuTrack"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('students.urls')),
    path('about/',views.about, name='about'),
    path('resource/delete/<int:id>/', views.delete_resource, name='delete_resource'),
    path('result/delete/<int:id>/', views.delete_result, name='delete_result'),
    path('grade/<str:grade_name>/print/', views.bulk_grade_report, name='bulk_grade_report'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)