from django.contrib import admin

from .models import Student, Subject, Teacher, Event, EventException, ChangeRequest

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Event)
admin.site.register(EventException)
admin.site.register(ChangeRequest)
