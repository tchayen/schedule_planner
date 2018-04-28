import itertools
from django.shortcuts import render
from django.db.models import Q
from datetime import datetime, timedelta
from itertools import groupby
from .models import Event
from django.core.mail import send_mail

def get_events(today):
    send_mail(
        'Subject',
        'Message.',
        'from@example.com',
        ['john@example.com', 'jane@example.com'],
    )

    first_day = today - timedelta(days=today.weekday())
    last_day = first_day + timedelta(days=5)
    events = [e for e in Event.objects.exclude(
        Q(end_date__lt=first_day) | \
        Q(end_date__isnull=True) | \
        Q(start_date__gte=last_day)).order_by('day_of_week', 'start_time')]

    days = []
    for key, group in itertools.groupby(events, lambda e: e.day_of_week):
        days.append(list(group))

    slots = [
        '08:00:00', '09:35:00', '11:15:00', '12:50:00',
        '14:40:00', '16:15:00', '17:50:00', '19:30:00',
    ]

    start_to_slot = dict(list(zip(slots, range(len(slots)))))

    result = []
    for index, day in enumerate(days):
        hour_slots = [[] for _ in range(len(slots))]
        for key, group in itertools.groupby(day, lambda e: start_to_slot[str(e.start_time)]):
            hour_slots[key] = list(group)
        result.append(hour_slots)

    print(result)
    return result


def index(request):
    days = get_events(datetime.today())

    context = { 'days': days }
    return render(request, 'planner/index.html', context)
