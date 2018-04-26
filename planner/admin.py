from django.contrib import admin

from .models import Student, Subject, Event, RecurringPattern, EventException

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Event)
admin.site.register(RecurringPattern)
admin.site.register(EventException)
