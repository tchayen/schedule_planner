import itertools
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime, timedelta
from itertools import groupby
from .models import Event

def get_events(today):
    first_day = today - timedelta(days=today.weekday())
    last_day = first_day + timedelta(days=5)
    events = [e for e in Event.objects.exclude(
        Q(end_date__lt=first_day) | \
        Q(end_date__isnull=True) | \
        Q(start_date__gte=last_day)).order_by('day_of_week')]

    events = sorted(events, key=lambda e: e.day_of_week)
    days = []
    for key, group in itertools.groupby(events, lambda e: e.day_of_week):
        days.append(list(group))

    return days


def index(request):
    days = get_events(datetime.today())

    context = { 'days': days }
    return render(request, 'planner/index.html', context)
