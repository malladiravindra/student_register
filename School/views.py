from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from .models import Teacher, Student, Attendance, Class, Subject
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def teacher_login(request):
    if request.method == 'POST':
        teacher_name = request.POST['teacher_name']
        password = request.POST['password']
        try:
            teacher = Teacher.objects.get(name=teacher_name)
            user = authenticate(request, username=teacher.user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('teacher_dashboard')
            else:
                messages.error(request, 'Invalid password.')
        except Teacher.DoesNotExist:
            messages.error(request, 'Teacher not found.')
    return render(request, 'login.html')

@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        teacher_name = data.get('teacher_name')
        password = data.get('password')
        try:
            teacher = Teacher.objects.get(name=teacher_name)
            user = authenticate(request, username=teacher.user.username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'teacher': {'id': teacher.id, 'name': teacher.name}})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid password.'})
        except Teacher.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Teacher not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid method.'})

@login_required
def teacher_dashboard(request):
    teacher = Teacher.objects.get(user=request.user)
    today = timezone.now().date()

    if request.method == 'POST':
        # Save attendance for all students in teacher's classes for today
        Attendance.objects.filter(date=today, teacher=teacher).delete()
        for key, value in request.POST.items():
            if not key.startswith('attendance_'):
                continue
            student_id = key.replace('attendance_', '')
            try:
                student = Student.objects.get(id=student_id, class_assigned__in=teacher.classes.all())
            except Student.DoesNotExist:
                continue
            is_present = value == 'present'
            Attendance.objects.create(
                student=student,
                date=today,
                is_present=is_present,
                teacher=teacher
            )
        messages.success(request, 'Attendance saved successfully.')
        return redirect('teacher_dashboard')

    # Get all students in teacher's classes
    students = Student.objects.filter(class_assigned__in=teacher.classes.all())

    # Get today's attendance for these students
    attendances = Attendance.objects.filter(
        student__in=students,
        date=today,
        teacher=teacher
    )

    # Group by subject or overall
    # For simplicity, assume one attendance per day per student
    attendance_dict = {att.student.id: att.is_present for att in attendances}
    
    # Build a list of student rows with attendance status
    student_rows = []
    for student in students:
        is_present = attendance_dict.get(student.id, False)
        student_rows.append({
            'student': student,
            'roll_number': student.roll_number,
            'name': student.name,
            'is_present': is_present,
            'status': 'Present' if is_present else 'Absent',
            'status_class': 'present' if is_present else 'absent',
        })

    total_students = students.count()
    present_students_list = [row for row in student_rows if row['is_present']]
    present_students = len(present_students_list)
    absent_students = total_students - present_students

    context = {
        'teacher': teacher,
        'student_rows': student_rows,
        'present_students_list': present_students_list,
        'total_students': total_students,
        'present_students': present_students,
        'absent_students': absent_students,
        'date': today,
    }
    return render(request, 'dashboard.html', context)

@login_required
def api_dashboard(request):
    teacher = Teacher.objects.get(user=request.user)
    today = timezone.now().date()

    students = Student.objects.filter(class_assigned__in=teacher.classes.all())
    attendances = Attendance.objects.filter(
        student__in=students,
        date=today,
        teacher=teacher
    )
    attendance_dict = {att.student.id: att.is_present for att in attendances}

    data = {
        'teacher': {'id': teacher.id, 'name': teacher.name},
        'date': today.isoformat(),
        'total_students': students.count(),
        'present_students': sum(1 for att in attendances if att.is_present),
        'absent_students': students.count() - sum(1 for att in attendances if att.is_present),
        'students': [{'id': s.id, 'name': s.name, 'roll_number': s.roll_number, 'class': s.class_assigned.name} for s in students],
        'attendance_dict': attendance_dict,
    }
    return JsonResponse(data)

@login_required
@csrf_exempt
def api_students(request):
    if request.method == 'GET':
        students = Student.objects.all().select_related('class_assigned')
        data = [{'id': s.id, 'name': s.name, 'roll_number': s.roll_number, 'phone_number': s.phone_number, 'class': s.class_assigned.name} for s in students]
        return JsonResponse({'students': data})
    elif request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        roll_number = data.get('roll_number')
        class_id = data.get('class_id')
        try:
            class_obj = Class.objects.get(id=class_id)
            phone_number = data.get('phone_number')
            student = Student.objects.create(name=name, roll_number=roll_number, phone_number=phone_number, class_assigned=class_obj)
            return JsonResponse({'success': True, 'student': {'id': student.id, 'name': student.name, 'roll_number': student.roll_number, 'phone_number': student.phone_number, 'class': student.class_assigned.name}})
        except Class.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Class not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid method.'})

@login_required
@csrf_exempt
def api_student_detail(request, pk):
    try:
        student = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Student not found.'}, status=404)
    
    if request.method == 'GET':
        data = {'id': student.id, 'name': student.name, 'roll_number': student.roll_number, 'phone_number': student.phone_number, 'class': student.class_assigned.name}
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        name = data.get('name')
        roll_number = data.get('roll_number')
        phone_number = data.get('phone_number')
        class_id = data.get('class_id')
        try:
            if name:
                student.name = name
            if roll_number:
                student.roll_number = roll_number
            if phone_number:
                student.phone_number = phone_number
            if class_id:
                class_obj = Class.objects.get(id=class_id)
                student.class_assigned = class_obj
            student.save()
            return JsonResponse({'success': True, 'student': {'id': student.id, 'name': student.name, 'roll_number': student.roll_number, 'phone_number': student.phone_number, 'class': student.class_assigned.name}})
        except Class.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Class not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    elif request.method == 'DELETE':
        student.delete()
        return JsonResponse({'success': True}, status=204)
    return JsonResponse({'success': False, 'error': 'Invalid method.'}, status=405)

@login_required
def api_classes(request):
    if request.method == 'GET':
        classes = Class.objects.all()
        data = [{'id': c.id, 'name': c.name} for c in classes]
        return JsonResponse({'classes': data})
    return JsonResponse({'success': False, 'error': 'Invalid method.'}, status=405)

@login_required
@csrf_exempt
def api_attendance(request):
    """
    GET: Get all students and their attendance status for today or a specific date
    POST: Mark multiple students as present/absent (bulk update)
    """
    teacher = Teacher.objects.get(user=request.user)
    
    if request.method == 'GET':
        date_str = request.GET.get('date')
        if not date_str:
            date_obj = timezone.now().date()
        else:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Get all students in teacher's classes
        students = Student.objects.filter(class_assigned__in=teacher.classes.all()).select_related('class_assigned')
        
        # Get today's attendance for these students
        attendances = Attendance.objects.filter(
            student__in=students,
            date=date_obj,
            teacher=teacher
        )
        
        attendance_dict = {att.student.id: att.is_present for att in attendances}
        
        data = {
            'date': date_obj.isoformat(),
            'teacher': {'id': teacher.id, 'name': teacher.name},
            'students': [
                {
                    'id': s.id,
                    'name': s.name,
                    'roll_number': s.roll_number,
                    'phone_number': s.phone_number,
                    'class': s.class_assigned.name,
                    'is_present': attendance_dict.get(s.id, None)
                }
                for s in students
            ],
            'total_students': students.count(),
            'present_count': sum(1 for att in attendances if att.is_present),
            'absent_count': sum(1 for att in attendances if not att.is_present),
        }
        return JsonResponse(data)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        date_str = data.get('date')
        present_student_ids = data.get('present', [])
        absent_student_ids = data.get('absent', [])
        
        if not date_str:
            date_obj = timezone.now().date()
        else:
            from datetime import datetime
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        try:
            # Delete existing attendance for this date and teacher
            Attendance.objects.filter(date=date_obj, teacher=teacher).delete()
            
            # Create attendance records for present students
            for student_id in present_student_ids:
                student = Student.objects.get(id=student_id)
                Attendance.objects.create(
                    student=student,
                    date=date_obj,
                    is_present=True,
                    teacher=teacher
                )
            
            # Create attendance records for absent students
            for student_id in absent_student_ids:
                student = Student.objects.get(id=student_id)
                Attendance.objects.create(
                    student=student,
                    date=date_obj,
                    is_present=False,
                    teacher=teacher
                )
            
            return JsonResponse({'success': True, 'message': 'Attendance recorded successfully'})
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'One or more students not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method.'}, status=405)

@login_required
@csrf_exempt
def api_attendance_detail(request, pk):
    """
    GET: Get attendance record for a specific student
    PUT: Update attendance for a specific student
    DELETE: Delete attendance record
    """
    teacher = Teacher.objects.get(user=request.user)
    
    try:
        attendance = Attendance.objects.get(id=pk, teacher=teacher)
    except Attendance.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Attendance record not found.'}, status=404)
    
    if request.method == 'GET':
        data = {
            'id': attendance.id,
            'student': {'id': attendance.student.id, 'name': attendance.student.name},
            'date': attendance.date.isoformat(),
            'is_present': attendance.is_present,
        }
        return JsonResponse(data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        is_present = data.get('is_present')
        
        if is_present is not None:
            attendance.is_present = is_present
            attendance.save()
            return JsonResponse({'success': True, 'message': 'Attendance updated successfully'})
        
        return JsonResponse({'success': False, 'error': 'is_present field is required.'})
    
    elif request.method == 'DELETE':
        attendance.delete()
        return JsonResponse({'success': True, 'message': 'Attendance record deleted.'}, status=204)
    
    return JsonResponse({'success': False, 'error': 'Invalid method.'}, status=405)

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

