from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

import exams
from .models import Exam, Question, Result
from django.contrib import messages   

def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'exams/exam_list.html', {'exams': exams})

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

    return render(request, 'exams/add_exam.html')

def add_question(request):
    exams = Exam.objects.all()

    if request.method == "POST":
        exam = Exam.objects.get(id=request.POST["exam"])

        Question.objects.create(
            exam=exam,
            question_text=request.POST["question_text"],
            option1=request.POST["option1"],
            option2=request.POST["option2"],
            option3=request.POST["option3"],
            option4=request.POST["option4"],
            correct_answer=request.POST["correct_answer"],
        )

        return redirect("add_question")

    return render(request, "exams/add_question.html", {"exams": exams})

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
            correct_option=getattr(question,question.correct_answer)

            print("Question:",question.question_text)
            print("Selected:", selected)
            print("Correct Answer:", correct_option)

            if selected == correct_option:
                score += question.marks
                print("Correct answer selected. Score updated to:", score)
            else:
                print("Incorrect answer selected. Score remains:", score)

        Result.objects.create(
            student=request.user,
            exam=exam,
            score=score
        )

        print("Final Score:", score)
        messages.success(request, "Exam submitted successfully!")

        return render(request, "students/submitted.html")
    return render(request, "exams/attempt_exam.html", {"exam": exam, "questions": questions})

def submitted(request):
    return render(request, "students/submitted.html")

def view_exams(request):    
    exams = Exam.objects.all()
    return render(request, 'exams/view_exams.html', {'exams':exams})