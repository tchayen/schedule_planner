from django.shortcuts import render

from .models import Student

def index(request):
    students_list = [s.first_name + ' ' + s.last_name for s in Student.objects.order_by('-last_name')]
    context = { 'students_list': students_list }
    return render(request, 'planner/index.html', context)

