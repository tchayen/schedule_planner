from django.contrib import admin

from .models import Student, Subject, Teacher, Event, SingularChange, ChangeRequest

admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Event)
admin.site.register(SingularChange)
admin.site.register(ChangeRequest)
