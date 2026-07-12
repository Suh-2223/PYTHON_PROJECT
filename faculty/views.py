from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth .models import User
from exams.models import Exam,Question,Result

def faculty_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('faculty_dashboard')

    return render(request, 'faculty/login.html')

def faculty_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            return redirect('faculty_login')

    return render(request, 'faculty/register.html')

def faculty_dashboard(request):
    return render(request, 'faculty/dashboard.html')

def add_exam(request):
    if request.method == 'POST':
        title = request.POST['title']
        subject = request.POST['subject']
        total_marks = request.POST['total_marks']
        duration = request.POST['duration']

        Exam.objects.create(
            title=title,
            subject=subject,
            total_marks=total_marks,
            duration=duration
        )

        return redirect('faculty_dashboard')

    return render(request, 'faculty/exam.html')

def add_question(request):
    if request.method == 'POST':
        exam_id = request.POST['exam_id']
        question_text = request.POST['question_text']
        option1 = request.POST['option1']
        option2 = request.POST['option2']
        option3 = request.POST['option3']
        option4 = request.POST['option4']
        correct_option = request.POST['correct_option']

        Question.objects.create(
            exam_id=exam_id,
            question_text=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option
        )

        return redirect('faculty_dashboard')

    return render(request, 'faculty/add_question.html')

def view_results(request):
   
    results = Result.objects.all()

    for result in results:
        result.percentage = round((result.score / result.exam.total_marks) * 100, 2)
        if result.percentage >= 50:
            result.status = "Pass"

        else:
            result.status = "Fail"
        print(f"Exam: {result.exam.title}, Student: {result.student.username}, Score: {result.score}, Percentage: {result.percentage}%")
    return render(request, 'faculty/view_results.html', {'results': results})




def attempt_exam(request, exam_id):
    print(request.method)   # Debug
    exam = get_object_or_404(Exam, id=exam_id)
    questions = Question.objects.filter(exam=exam)

    if request.method == 'POST':
        print("POST RECEIVED")  
        print(request.POST)  # Debug
        score = 0
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option == question.correct_option:
                score += 1

        Result.objects.create(
            student=request.user,
            exam=exam,
            score=score
        )

        print("RESULT SAVED")
        messages.success(request, 'Your exam has been submitted successfully.')

        return render(request, 'students/submitted.html')



    return render(request, 'exams/attempt_exam.html', {
        'exam': exam,
        'questions': questions
    })

def logout_view(request):
    logout(request)
    return redirect('/')