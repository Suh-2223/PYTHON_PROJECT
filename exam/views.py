from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

def home(request):
    return render(request, 'home.html')

def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(username="admin", email="admin@example.com", password="Admin@123")

        return HttpResponse("Superuser created successfully.")
    return HttpResponse("Superuser already exists.")