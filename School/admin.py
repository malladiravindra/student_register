from django.contrib import admin
from .models import Class, Subject, Teacher, Student, Attendance

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    filter_horizontal = ('classes', 'subjects')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'class_assigned')
    list_filter = ('class_assigned',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present', 'teacher', 'subject')
    list_filter = ('date', 'is_present', 'teacher', 'subject')