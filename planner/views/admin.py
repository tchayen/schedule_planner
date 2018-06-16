from django.shortcuts import render
from ..models import ChangeRequest
from .change_request import description

def add_description(cr):
    cr.description = description(cr)
    return cr

def admin(request):
    change_requests = [cr for cr in ChangeRequest.objects.all().order_by('created_at')]
    change_requests = map(add_description, change_requests)

    context = { 'change_requests': change_requests }
    return render(request, 'planner/admin.html', context)
