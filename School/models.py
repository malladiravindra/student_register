from django.db import models
from django.contrib.auth.models import User

class Class(models.Model):
    name = models.CharField(max_length=20, unique=True)  # e.g., "1st", "2nd", ..., "10th"

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    # Assigned classes and subjects
    classes = models.ManyToManyField(Class, blank=True, related_name='teachers')
    subjects = models.ManyToManyField(Subject, blank=True, related_name='teachers')

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'date', 'subject')  # Assuming attendance per subject per day

    def __str__(self):
        return f"{self.student} - {self.date} - {self.subject} - {'Present' if self.is_present else 'Absent'}"