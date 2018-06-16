from django.shortcuts import redirect
from ..models import EventException, ChangeRequest
from django.views.decorators.csrf import csrf_protect

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
