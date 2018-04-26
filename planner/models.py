from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Student(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    """{start,end}_date fields are designated to store the first time event
    has occured (most of the time it will be the beginning of the semester)
    """
    start_date = models.DateField(default=None, blank=True, null=True)
    end_date = models.DateField(default=None, blank=True, null=True)

    """{start,end}_time fields are supposed to show timespan of the classes"""
    start_time = models.DateTimeField(default=None, blank=True, null=True)
    end_time = models.DateTimeField(default=None, blank=True, null=True)


class RecurringPattern(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    max_occurences = models.IntegerField()
    separation_count = models.IntegerField()
    day_of_week = models.IntegerField()


class EventException(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start_date = models.DateField(default=None, blank=True, null=True)
    end_date = models.DateField(default=None, blank=True, null=True)
    start_time = models.DateTimeField(default=None, blank=True, null=True)
    end_time = models.DateTimeField(default=None, blank=True, null=True)
