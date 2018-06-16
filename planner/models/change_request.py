from django.db import models
from django.utils import timezone
from .student import Student
from .event import Event

class ChangeRequest(models.Model):
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(ChangeRequest, self).save(*args, **kwargs)

    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    updated_at = models.DateTimeField()
    created_at = models.DateTimeField(editable=False)

    """The day since which the change will take place."""
    change_start_date = models.DateField()
    change_end_date = models.DateField(default=None, blank=True, null=True)

    """New start and end of the event. Might be null if it is not affected."""
    new_start_time = models.TimeField(default=None, blank=True, null=True)
    new_end_time = models.TimeField(default=None, blank=True, null=True)

    new_day_of_week = models.IntegerField(blank=True, null=True)

    one_time_change = models.BooleanField(default=False)
    accepted = models.NullBooleanField(blank=True, null=True)
