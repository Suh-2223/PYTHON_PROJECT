from exams.models import Exam
from django.shortcuts import render

def view_exams(request):
    exams = Exam.objects.all()
    return render(request, "accounts/view_exams.html", {"exams": exams})