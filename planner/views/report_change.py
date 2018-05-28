from django.shortcuts import render
from ..models import ChangeRequest
from ..forms import ReportChangeForm

def report_change(request):
    change_requests = [cr for cr in ChangeRequest.objects
        .filter(author=request.user.id)
        .order_by('created_at')]

    context = { 'change_requests': change_requests }
    return render(request, 'planner/report_change.html', context)

def new_report_change(request, id):
    if request.method == 'POST':
        form = ReportChangeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/report_change')

    return render(request, 'planner/new_report_change.html', {})
