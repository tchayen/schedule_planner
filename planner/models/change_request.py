from django.db import models
from .student import Student
from .event import Event

class ChangeRequest(models.Model):
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
