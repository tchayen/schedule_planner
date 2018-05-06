from django.shortcuts import render
from ..models import ChangeRequest

def admin(request):
    change_requests = [cr for cr in ChangeRequest.objects.all().order_by('created_at')]

    context = { 'change_requests': change_requests }
    return render(request, 'planner/admin.html', context)
