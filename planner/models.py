from django.db import models


def week_day():
    return ['pon', 'wto', 'śro', 'czw', 'pią']


class Subject(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    parent_event = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    """{start,end}_date fields are designated to store the first time event
    has occured (most of the time it will be the beginning of the semester)
    """
    start_date = models.DateField(default=None, blank=True, null=True)
    end_date = models.DateField(default=None, blank=True, null=True)

    """{start,end}_time fields are supposed to show timespan of the classes"""
    start_time = models.DateTimeField(default=None, blank=True, null=True)
    end_time = models.DateTimeField(default=None, blank=True, null=True)

    """Determine amount of N weeks between each event (in most of the cases: 1 or 2)"""
    separation_count = models.IntegerField(default=1)

    day_of_week = models.IntegerField(null=True)

    def __str__(self):
        return self.subject.name + ' ' + week_day()[self.day_of_week] + ' ' + self.start_time.strftime('%H:%M') + ' - ' + self.end_time.strftime('%H:%M')


class Group(models.Model):
    students = models.ManyToManyField(Student, blank=True)
    classes = models.ManyToManyField(Event, blank=True)


class RecurringPattern(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    max_occurences = models.IntegerField()


class EventException(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start_date = models.DateField(default=None, blank=True, null=True)
    end_date = models.DateField(default=None, blank=True, null=True)
    start_time = models.DateTimeField(default=None, blank=True, null=True)
    end_time = models.DateTimeField(default=None, blank=True, null=True)
