from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='student_register'),
    path('login/', views.student_login, name='student_login'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('view_results/', views.view_results, name='student_view_results'),
    path('exam/', views.exam_list, name='exam_list'),
    path('exam/<int:exam_id>/', views.attempt_exam, name='attempt_exam'),

]