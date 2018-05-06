import itertools
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime, timedelta
from itertools import groupby
from .models import Event, EventException, ChangeRequest
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

def slots():
    return [
        '08:00:00', '09:35:00', '11:15:00', '12:50:00',
        '14:40:00', '16:15:00', '17:50:00', '19:30:00',
    ]

def check_exceptions(event, event_exceptions):
    condition = True
    for e in event_exceptions:
        date = event.start_date

        while date < e.replaced_date and date < event.end_date:
            date += timedelta(days=7) * event.separation_count

        if date == event:
            condition = False

    return condition


def exceptions_to_events(event_exceptions):
    events = []
    for e in event_exceptions:
        event = Event()
        event.start_date = event.end_date = e.new_date
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

    events += event_models

    # Filter out events moved by exceptions
    events = [e for e in events if check_exceptions(e, event_exceptions)]

    # Add exceptions as new events
    events += exceptions_to_events(event_exceptions)

    # Group events by days
    days = []
    for key, group in itertools.groupby(events, lambda e: e.day_of_week):
        days.append(list(group))

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


@csrf_protect
def change_request(request, id, decision):
    cr = ChangeRequest.objects.get(pk=id)
    cr.accepted = True if decision == 'accept' else False
    cr.save()

    if cr.accepted:
        return redirect(to='/admin')

    if cr.one_time_change:
        # TODO: fix
        ex = EventException()
        ex.event = cr.event
        ex.replaced_date = cr.change_start_date
        ex.new_date = cr.change_start_date

        if cr.new_start_time and cr.new_end_time:
            ex.start_time = cr.new_start_time
            ex.end_time = cr.new_end_time
        else:
            ex.start_time = cr.event.start_time
            ex.end_time = cr.event.end_time

        if cr.new_day_of_week:
            ex.day_of_week = cr.new_day_of_week
        else:
            ex.day_of_week = cr.event.day_of_week

        print(ex.__dict__)
        ex.save()

    # TODO: handle other cases

    return redirect(to='/admin')


def admin(request):
    change_requests = [cr for cr in ChangeRequest.objects.all().order_by('created_at')]

    context = { 'change_requests': change_requests }
    return render(request, 'planner/admin.html', context)
