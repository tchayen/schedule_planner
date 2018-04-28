from django.db import models
from .student import Student
from .event import Event

def week_day():
    return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

class ChangeRequest(models.Model):
    author = models.ForeignKey(Student, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    """The day since which the change will take place."""
    change_start_date = models.DateField()
    change_end_date = models.DateField(default=None, blank=True, null=True)

    """New start and end of the event. Might be null if it is not affected."""
    new_start_time = models.TimeField(default=None, blank=True, null=True)
    new_end_time = models.TimeField(default=None, blank=True, null=True)

    new_day_of_week = models.IntegerField(blank=True, null=True)

    one_time_change = models.BooleanField(default=False)

    def description(self):
        subject = self.event.subject

        start_date_string = self.change_start_date.strftime('%Y-%m-%d')
        if self.change_end_date:
            end_date_string = self.change_end_date.strftime('%Y-%m-%d')
            end_string = 'until <strong>{0}</strong>'.format(end_date_string)
        else:
            end_string = 'until the end of the semester'

        if self.new_start_time and self.new_end_time:
            start_time_string = self.new_start_time.strftime('%H:%M')
            end_time_string = self.new_end_time.strftime('%H:%M')

        weekday = week_day()[self.new_day_of_week] if self.new_day_of_week \
            else week_day()[self.event.day_of_week]

        once = 'once' if self.one_time_change else end_string

        if self.new_start_time and self.new_end_time:
            return ('Move <strong>{0}</strong> to <strong>{1} {2}</strong>, {3}, ' + \
                'starting from <strong>{4}</strong>').format(
                subject,
                weekday,
                start_time_string + ' - ' + \
                end_time_string,
                once,
                self.change_start_date
            )

        if self.new_day_of_week:
            return ('Change day of the week for <strong>{0}</strong> to ' + \
                '<strong>{1}</strong>, {2}, {3} <strong>{4}</strong> {5}').format(
                subject,
                weekday,
                once,
                'at' if self.one_time_change else 'since',
                start_date_string,
                'to <strong>' + end_date_string + \
                '</strong>' if self.change_end_date else ''
            )

        return 'No change'