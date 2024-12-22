

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

    path('register/student/', views.register_student, name='register_student'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),

    # Dashboards
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # Student Views
    path('register_units/', views.register_units, name='register_units'),
    path('submit_assignment/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('report_session/', views.report_session, name='report_session'),

    # Teacher Views
    path('post_assignment/', views.post_assignment, name='post_assignment'),
    path('students_in_unit/<int:unit_id>/', views.students_in_unit, name='students_in_unit'),
    path('view_submissions/<int:assignment_id>/', views.view_submissions, name='view_submissions'),
]
