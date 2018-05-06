from django.db import models
from .event import Event

class EventException(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    replaced_date = models.DateField()
    new_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
