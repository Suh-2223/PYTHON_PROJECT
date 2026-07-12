from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.faculty_login, name='faculty_login'),
    path('register/', views.faculty_register, name='faculty_register'),
    path('dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('view_results/', views.view_results, name='faculty_view_results'),
    path('logout/', views.logout_view, name='logout'),
    path('add_question/', views.add_question, name='add_question'),
    path('add_exam/', views.add_exam, name='add_exam'),
   

]
