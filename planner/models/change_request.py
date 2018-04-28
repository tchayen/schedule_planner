from django.db import models
from .student import Student
from .event import Event

class ChangeRequest(models.Model):
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    """The day since which the change will take place."""
    change_start_date = models.DateField()
    change_end_date = models.DateField(default=None, blank=True, null=True)

    """New start and end of the event. Might be null if it is not affected."""
    new_start_time = models.TimeField(default=None, blank=True, null=True)
    new_end_time = models.TimeField(default=None, blank=True, null=True)

    new_day_of_week = models.IntegerField(null=True)

    one_time_change = models.BooleanField(default=False)
