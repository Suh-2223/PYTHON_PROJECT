from django.db import models
from students.models import Student

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    obtained_marks = models.IntegerField()
    percentage = models.FloatField()
    exam_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.student.name
