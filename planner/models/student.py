from django.db import models
from .event import Event

class Student(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    classes = models.ManyToManyField(Event, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
