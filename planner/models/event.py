from django.db import models
from .subject import Subject
from .teacher import Teacher

def week_day():
    return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

class Event(models.Model):
    parent_event = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    """{start,end}_time fields are designated to store the first time event
    has occured (most of the time it will be the beginning of the semester)
    """
    start_date = models.DateField(default=None)
    end_date = models.DateField(default=None, blank=True, null=True)

    """{start,end}_time fields are supposed to show timespan of the classes"""
    start_time = models.TimeField(default=None)
    end_time = models.TimeField(default=None)

    """Determine amount of N weeks between each event (in most of the cases: 1 or 2)"""
    separation_count = models.IntegerField(default=1)

    day_of_week = models.IntegerField(null=True)

    def timespan(self):
        return self.start_time.strftime('%H:%M') + ' - ' + self.end_time.strftime('%H:%M')

    def __str__(self):
        return self.subject.name + ' ' + week_day()[self.day_of_week] + ' ' + self.timespan()
