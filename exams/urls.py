from django.urls import path
from . import views

urlpatterns = [
    # path('view_exams/', views.exam_list, name='exam_list'),
    path('add_exam/', views.add_exam, name='add_exam'),
    path('add_question/', views.add_question, name='add_question'),
    path('attempt_exam/<int:exam_id>/', views.attempt_exam, name='attempt_exam'),
    path('view_exams/', views.view_exams, name='view_exams'),
    path('create_admin/', views.create_admin, name='create_admin'),


]