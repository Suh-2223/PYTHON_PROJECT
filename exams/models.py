from django.db import models

class Exam(models.Model):
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    total_marks = models.IntegerField()
    duration = models.IntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.title

    

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question_text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)
    marks = models.IntegerField(default=5)

    def __str__(self):
        return self.question_text
    
class Result(models.Model):
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField()
    

    def __str__(self):
  
        return f"{self.student.username} - {self.exam.title} - {self.score}"

