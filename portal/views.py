from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from portal.models import CustomUser

# User Registration View
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validation checks
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')
        
        # Create user using CustomUser model
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')
    
    return render(request, 'auth/register.html')


# User Login View


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User

def user_login(request):
  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')

    # Log the provided username and password (for debugging purposes)
    print(f"Attempting login with username: {username}")

    # Authenticate the user
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
      login(request, user)
      print(f"User {username} logged in successfully.")
      
      # Redirect based on user role (assuming student/teacher dashboards exist)
      if user.is_student:
        return redirect('student_dashboard')
      elif user.is_teacher:
        return redirect('teacher_dashboard')
      else:
        messages.error(request, "Invalid user role.")
        return redirect('login')
    else:
      messages.error(request, "Invalid username or password.")
      print(f"Failed login attempt for username: {username}")
      return redirect('login')
  
  return render(request, 'auth/login.html')

# User Logout View
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')



@login_required
def register_units(request):
    if not request.user.is_student:
        return redirect('login')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.student = request.user
            registration.save()
            return redirect('student_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'portal/register_units.html', {'form': form})


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True  # Assign role as student
            user.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = StudentRegistrationForm()
    return render(request, 'auth/register_student.html', {'form': form})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_teacher = True  # Assign role as teacher
            user.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = TeacherRegistrationForm()
    return render(request, 'auth/register_teacher.html', {'form': form})



@login_required
def submit_assignment(request, assignment_id):
    if not request.user.is_student:
        return redirect('login')
    assignment = Assignment.objects.get(id=assignment_id)
    if request.method == 'POST':
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            return redirect('student_dashboard')
    else:
        form = AssignmentSubmissionForm()
    return render(request, 'portal/submit_assignment.html', {'form': form, 'assignment': assignment})


@login_required
def students_in_unit(request, unit_id):
    if not request.user.is_teacher:
        return redirect('login')
    unit = Unit.objects.get(id=unit_id)
    registrations = Registration.objects.filter(unit=unit)
    return render(request, 'portal/students_in_unit.html', {'unit': unit, 'registrations': registrations})


@login_required
def view_submissions(request, assignment_id):
    if not request.user.is_teacher:
        return redirect('login')
    assignment = Assignment.objects.get(id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    return render(request, 'portal/view_submissions.html', {'assignment': assignment, 'submissions': submissions})


@login_required
def report_session(request):
    if not request.user.is_student:
        return redirect('login')
    # Logic for reporting the session
    # Example: Just a confirmation page
    if request.method == 'POST':
        # Handle session reporting logic
        return redirect('student_dashboard')
    return render(request, 'portal/report_session.html')

# Student Dashboard
@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return redirect('login')
    registrations = Registration.objects.filter(student=request.user)
    assignments = Assignment.objects.filter(unit__in=[reg.unit for reg in registrations])
    return render(request, 'portal/student_dashboard.html', {'registrations': registrations, 'assignments': assignments})

# Teacher Dashboard
@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        return redirect('login')
    units = Unit.objects.filter(teacher=request.user)
    return render(request, 'portal/teacher_dashboard.html', {'units': units})

# Post Assignment
@login_required
def post_assignment(request):
    if not request.user.is_teacher:
        return redirect('login')

    if request.method == 'POST':
        unit_id = request.POST.get('unit')
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES['file']
        try:
            unit = Unit.objects.get(id=unit_id, teacher=request.user)
            Assignment.objects.create(unit=unit, title=title, description=description, file=file)
            return redirect('teacher_dashboard')
        except Unit.DoesNotExist:
            messages.error(request, "Invalid unit selected.")
            return redirect('post_assignment')

    units = Unit.objects.filter(teacher=request.user)
    print(f"Number of units: {units.count()}")  # Debug print
    print(f"Units: {units}") #Debug print to show the units
    return render(request, 'portal/post_assignment.html', {'units': units})