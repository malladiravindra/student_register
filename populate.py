import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'School.settings')
django.setup()

from School.models import Class, Subject, Teacher, Student, Attendance
from datetime import date

# Create classes
classes = []
for i in range(1, 11):
    suffix = 'st' if i == 1 else 'nd' if i == 2 else 'rd' if i == 3 else 'th'
    name = f"{i}{suffix}"
    cls, created = Class.objects.get_or_create(name=name)
    classes.append(cls)

# Create subjects
subjects = []
subj_names = ['Mathematics', 'English', 'Science', 'History', 'Geography']
for name in subj_names:
    subj, created = Subject.objects.get_or_create(name=name)
    subjects.append(subj)

# Create teachers
teachers = []
teacher_names = ['Mr. Smith', 'Ms. Johnson', 'Mr. Brown', 'Ms. Davis', 'Mr. Wilson']
for i, name in enumerate(teacher_names):
    user, created = User.objects.get_or_create(username=f'teacher{i+1}', defaults={'email': f'teacher{i+1}@school.com'})
    if created:
        user.set_password('password123')
        user.save()
    teacher, created = Teacher.objects.get_or_create(user=user, defaults={'name': name})
    # Assign classes and subjects
    start = i * 2
    end = (i + 1) * 2
    teacher.classes.set(classes[start:end])  # Each teacher to 2 classes
    teacher.subjects.set([subjects[i]])  # Each to one subject
    teacher.save()
    teachers.append(teacher)

# Create students
students = []
for cls in classes:
    for j in range(1, 11):  # 10 students per class
        roll = f"{cls.name[0]}{j:02d}"
        student, created = Student.objects.get_or_create(
            roll_number=roll,
            defaults={'name': f"Student {roll}", 'class_assigned': cls}
        )
        students.append(student)

# Create some attendance for today
today = date.today()
for idx, student in enumerate(students[:50]):  # For first 50 students
    teacher = teachers[idx % len(teachers)]  # Cycle through teachers
    subject = subjects[idx % len(subjects)]
    Attendance.objects.get_or_create(
        student=student,
        date=today,
        teacher=teacher,
        subject=subject,
        defaults={'is_present': True}
    )

print("Sample data created.")