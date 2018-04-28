import itertools
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime, timedelta
from itertools import groupby
from .models import Event, ChangeRequest
from django.core.mail import send_mail
from django.shortcuts import redirect

def slots():
    return [
        '08:00:00', '09:35:00', '11:15:00', '12:50:00',
        '14:40:00', '16:15:00', '17:50:00', '19:30:00',
    ]

def get_events(first_day, last_day):
    events = [e for e in Event.objects.exclude(
        Q(end_date__lt=first_day) | \
        Q(end_date__isnull=True) | \
        Q(start_date__gte=last_day)).order_by('day_of_week', 'start_time')]

    # Group events by days
    days = []
    for key, group in itertools.groupby(events, lambda e: e.day_of_week):
        days.append(list(group))

    # Add arrays containing time slots
    start_to_slot = dict(list(zip(slots(), range(len(slots())))))

    result = []
    for index, day in enumerate(days):
        hour_slots = [[] for _ in range(len(slots()))]
        for key, group in itertools.groupby(day,
            lambda e: start_to_slot[str(e.start_time)]):
            hour_slots[key] = list(group)
        result.append(hour_slots)

    return result


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


def change_request(request, id, decision):
    change_request = ChangeRequest.objects.get(pk=id)
    change_request.accepted = True if decision == 'accept' else False
    change_request.save()
    return redirect(to='/admin')


def admin(request):
    change_requests = [cr for cr in ChangeRequest.objects.all().order_by('created_at')]

    context = { 'change_requests': change_requests }
    return render(request, 'planner/admin.html', context)
