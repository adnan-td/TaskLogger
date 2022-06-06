from django.db import models
from django.contrib.auth.models import User


class Section(models.Model):
    college = models.CharField(max_length=252, null=True)
    branch = models.CharField(max_length=252, null=True)
    section = models.CharField(max_length=252, null=True)

    def __str__(self):
        return str(self.college) + ' ' + str(self.branch) + ' ' + str(self.section)


class Student(models.Model):
    student_username = models.CharField(
        "Your Username", max_length=252, null=True)
    student_section = models.ForeignKey(Section, on_delete=models.PROTECT)
    student_name = models.CharField("Name", max_length=252, null=True)
    student_rollno = models.IntegerField("Roll No")

    def __str__(self):
        return self.student_name


class SectionEvent(models.Model):
    name_choices = (("1", "Mon"), ("2", "Tue"), ("3", "Wed"), ("4", "Thu"),
                    ("5", "Fri"), ("6", "Sat"), ("7", "Sun"), ("8", "Other"))
    name = models.CharField("Day", max_length=3, choices=name_choices)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=252)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField()

    def __str__(self):
        return self.event_name


class PEvent(models.Model):
    pevents = models.ForeignKey(Student, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=252)
    date = models.DateField()
    time = models.TimeField()
    dateTime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.event_name
