from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Course(models.Model):
    name = models.CharField(max_length=100)
    SEMESTER = (("1st", "First Semester"), ("2nd", "Second Semester"))
    code = models.CharField(max_length=10, unique=True)
    sem = models.CharField(max_length=10, choices=SEMESTER)
    elective = models.BooleanField(default=False)
    unit = models.IntegerField(default=2)

    def __str__(self):
        return self.name


class Registration(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(null=True)

    # def __str__(self):
    #     return str(self.student) + " had " + str(self.score) + " in " + str(self.course)
