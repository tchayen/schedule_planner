from django.shortcuts import redirect
from ..models import SingularChange, ChangeRequest
from django.views.decorators.csrf import csrf_protect

def description(request):
    # Alias variables
    subject = request.event.subject

    start_date_string = request.change_start_date.strftime('%Y-%m-%d')

    if request.change_end_date:
        end_date_string = request.change_end_date.strftime('%Y-%m-%d')
        end_string = 'until <strong>{0}</strong>'.format(end_date_string)
    else:
        end_string = 'until the end of the semester'

    if request.new_start_time and request.new_end_time:
        start_time_string = request.new_start_time.strftime('%H:%M')
        end_time_string = request.new_end_time.strftime('%H:%M')

    weekday = week_day()[request.new_day_of_week] if request.new_day_of_week \
        else week_day()[request.event.day_of_week]

    once = 'once' if request.one_time_change else end_string

    # Print final string based on the data
    if request.new_start_time and request.new_end_time:
        return ('Move <strong>{0}</strong> to <strong>{1} {2}</strong>, {3}, ' + \
            'starting from <strong>{4}</strong>').format(
            subject,
            weekday,
            start_time_string + ' - ' + \
            end_time_string,
            once,
            request.change_start_date
        )

    if request.new_day_of_week:
        return ('Change day of the week for <strong>{0}</strong> to ' + \
            '<strong>{1}</strong>, {2}, {3} <strong>{4}</strong> {5}').format(
            subject,
            weekday,
            once,
            'at' if request.one_time_change else 'since',
            start_date_string,
            'to <strong>' + end_date_string + \
            '</strong>' if request.change_end_date else ''
        )

    return 'No change'

@csrf_protect
def change_request(request, id, decision):
    cr = ChangeRequest.objects.get(pk=id)
    cr.accepted = True if decision == 'accept' else False
    cr.save()

    if cr.accepted:
        return redirect(to='/admin')

    if cr.one_time_change:
        ex = SingularChange()
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

    return redirect(to='/admin')
