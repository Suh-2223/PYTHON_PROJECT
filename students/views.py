from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from accounts.views import view_exams
from exams.models import Exam,Question, Result
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("student_register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("student_register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("student_register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Student registered successfully.")
        return redirect("student_login")

    return render(request, "students/register.html")
       



def student_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("student_dashboard")
    

    return render(request, "students/login.html")

def student_dashboard(request):
    return render(request, "students/dashboard.html")

def exam_list(request,exam_id):
        exams = get_object_or_404(Exam, id=exam_id)
        return render(request, 'students/attempt_exam.html', {'exams': exams})

def attempt_exam(request, exam_id):
    print(request.method)   # Debug

    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam)

    if request.method == "POST":
        print("POST RECEIVED")  
        print(request.POST)  # Debug

        score = 0

        for question in questions:
            selected = request.POST.get(str(question.id))
            print(question.id, selected)

            if selected == question.correct_answer:
                score += question.marks

        Result.objects.create(
            student=request.user,
            exam=exam,
            score=score
        )

        print("RESULT SAVED")
        messages.success(request, "Exam submitted successfully!")

        return render(request, "students/submitted.html")
        return render(request, "exams/attempt_exam.html", {"exam": exam, "questions": questions})



    exam =get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam)

    if request.method == 'POST':
        total_marks = 0
        for question in questions:
            selected_option = request.POST.get(f'question_{question.id}')
            if selected_option == question.correct_option:
                total_marks += question.marks

        Result.objects.create(
            student=request.user,
            exam=exam,
            marks_obtained=total_marks
        )
        return render(request, 'students/attempt_exam.html', {'exam': exam, 'questions': questions})
        return render(request, 'students/attempt_exam.html', {'exam': exam, 'questions': questions})


def view_results(request):
   
    results = Result.objects.filter(student=request.user)

    for result in results:
        result.percentage = round((result.score / result.exam.total_marks) * 100, 2)
        if result.percentage >= 50:
            result.status = "Pass"
        else:
            result.status = "Fail"
        print(f"Exam: {result.exam.title}, Score: {result.score}, Percentage: {result.percentage}%")
    return render(request, 'students/results.html', {'results': results})
