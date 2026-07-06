import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'School.settings')
django.setup()

from School.models import Student, Class
import random

# List of realistic Indian names
first_names = [
    'Rajesh', 'Priya', 'Arun', 'Divya', 'Suresh', 'Anjali', 'Vikram', 'Neha',
    'Ashok', 'Pooja', 'Ramesh', 'Sunita', 'Arjun', 'Kavya', 'Sanjay', 'Deepa',
    'Rohan', 'Isha', 'Varun', 'Meera', 'Harish', 'Sneha', 'Ravi', 'Shreya',
    'Nitin', 'Ananya', 'Ajay', 'Ritika', 'Harsh', 'Sakshi', 'Akshay', 'Vanya',
    'Kunal', 'Diya', 'Aman', 'Mira', 'Abhishek', 'Nidhi', 'Ronak', 'Priyanka',
    'Vivek', 'Swati', 'Siddharth', 'Anushka', 'Manish', 'Tanvi', 'Puneet', 'Aarav'
]

last_names = [
    'Kumar', 'Singh', 'Sharma', 'Patel', 'Gupta', 'Reddy', 'Joshi', 'Verma',
    'Nair', 'Menon', 'Desai', 'Rao', 'Bhat', 'Chopra', 'Kapoor', 'Malhotra'
]

# Get the first class or create one
try:
    class_obj = Class.objects.first()
    if not class_obj:
        class_obj = Class.objects.create(name='1st')
except:
    class_obj = Class.objects.create(name='1st')

# Generate 50 students
students_created = 0

for i in range(1, 51):
    roll_number = f'209T1A0{500 + i}'
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    name = f'{first_name} {last_name}'
    phone_number = f'98{random.randint(10000000, 99999999)}'
    
    # Check if student already exists
    if not Student.objects.filter(roll_number=roll_number).exists():
        student = Student.objects.create(
            name=name,
            roll_number=roll_number,
            phone_number=phone_number,
            class_assigned=class_obj
        )
        students_created += 1
        print(f'Created: {name} | Roll: {roll_number} | Phone: {phone_number}')
    else:
        print(f'Already exists: {roll_number}')

print(f'\nTotal students created: {students_created}')
