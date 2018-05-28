import itertools
from operator import attrgetter
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime, timedelta
from itertools import groupby
from ..models import Event, EventException, ChangeRequest

class CalendarEvent():
    def timespan(self):
        return self.start_time.strftime('%H:%M') + ' - ' + self.end_time.strftime('%H:%M')

    def __str__(self):
        return ""

def slots():
    return [
        '08:00:00', '09:35:00', '11:15:00', '12:50:00',
        '14:40:00', '16:15:00', '17:50:00', '19:30:00',
    ]

def check_exceptions(event, event_exceptions):
    for e in event_exceptions:
        if event.date == e.replaced_date:
            return False
    return True


def models_to_events(models, first_day, last_day):
    first_day = first_day.date()
    last_day = last_day.date()

    events = []
    for m in models:
        date = m.start_date - timedelta(days=m.start_date.weekday()) + \
            timedelta(days=7) + timedelta(days=m.day_of_week)

        while date < last_day:
            if date >= first_day:
                event = CalendarEvent()

                event.id = m.id
                event.date = date,
                event.start_time = m.start_time
                event.end_time = m.end_time
                event.day_of_week = m.day_of_week
                event.subject = m.subject
                event.teacher = m.teacher

                events.append(event)

            date += timedelta(days=7) * m.separation_count
    return events


def exceptions_to_events(event_exceptions):
    events = []
    for e in event_exceptions:
        event = CalendarEvent()

        event.date = e.new_date
        event.start_time = e.start_time
        event.end_time = e.end_time
        event.subject = e.event.subject
        event.teacher = e.event.teacher
        event.day_of_week = e.new_date.weekday()

        events.append(event)

    return events


def get_events(first_day, last_day):
    events = []

    # Fetch event models
    event_models = [e for e in Event.objects.exclude(
        Q(end_date__lt=first_day) | \
        Q(start_date__gte=last_day)
    ).order_by('day_of_week', 'start_time')]

    event_exceptions = [ee for ee in EventException.objects.filter(
        new_date__range=(first_day, last_day))]

    events += models_to_events(event_models, first_day, last_day)
    events = [e for e in events if check_exceptions(e, event_exceptions)]
    events += exceptions_to_events(event_exceptions)
    events = sorted(events, key=attrgetter('day_of_week', 'start_time'))

    # Group events by days
    days = [[] for _ in range(5)]
    for key, group in itertools.groupby(events, lambda e: e.day_of_week):
        days[key] = list(group)

    # Add arrays containing time slots
    start_to_slot = dict(list(zip(slots(), range(len(slots())))))

    results = []
    for index, day in enumerate(days):
        hour_slots = [[] for _ in range(len(slots()))]
        for key, group in itertools.groupby(day,
            lambda e: start_to_slot[str(e.start_time)]):
            hour_slots[key] = list(group)
        results.append(hour_slots)

    return results


def index(request):
    today = datetime.today()
    first_day = today - timedelta(days=today.weekday())

    # If it is already weekend, show the next week
    if today.weekday() >= 5:
        first_day = first_day + timedelta(days=7)

    last_day = first_day + timedelta(days=5)

    previous_week = first_day - timedelta(days=7)
    next_week = first_day + timedelta(days=7)

    result = get_events(first_day, last_day)
    context = {
        'days': result,
        'first_day': first_day.strftime('%Y-%m-%d'),
        'last_day': last_day.strftime('%Y-%m-%d'),
        'previous_week': previous_week.strftime('%Y-%m-%d'),
        'next_week': next_week.strftime('%Y-%m-%d'),
    }
    return render(request, 'planner/index.html', context)


def calendar(request, first_day):
    first_day = datetime.strptime(first_day, '%Y-%m-%d')
    last_day = first_day + timedelta(days=5)

    previous_week = first_day - timedelta(days=7)
    next_week = first_day + timedelta(days=7)

    if first_day.weekday() != 0:
        raise ValueError('Provided day must be monday')

    result = get_events(first_day, last_day)
    context = {
        'days': result,
        'first_day': first_day.strftime('%Y-%m-%d'),
        'last_day': last_day.strftime('%Y-%m-%d'),
        'previous_week': previous_week.strftime('%Y-%m-%d'),
        'next_week': next_week.strftime('%Y-%m-%d'),
    }
    return render(request, 'planner/index.html', context)
