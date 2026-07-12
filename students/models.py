from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_no = models.CharField(max_length=20, unique=True)
    course = models.CharField(max_length=50)

    def _str_(self):
        return self.name



