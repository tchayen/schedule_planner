from django.db import models
from .event import Event

class EventException(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=None)
    end_time = models.DateTimeField(default=None)
