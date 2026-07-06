"""
URL configuration for School project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.teacher_login, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', views.teacher_login, name='teacher_login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('api/login/', views.api_login, name='api_login'),
    path('api/dashboard/', views.api_dashboard, name='api_dashboard'),
    path('api/students/', views.api_students, name='api_students'),
    path('api/students/<int:pk>/', views.api_student_detail, name='api_student_detail'),
    path('api/classes/', views.api_classes, name='api_classes'),
    path('api/attendance/', views.api_attendance, name='api_attendance'),
    path('api/attendance/<int:pk>/', views.api_attendance_detail, name='api_attendance_detail'),
]
