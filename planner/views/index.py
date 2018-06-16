import itertools
from operator import attrgetter
from django.shortcuts import render
from datetime import datetime, timedelta
from ..utils import get_events

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
