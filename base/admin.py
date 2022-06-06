from django.contrib import admin
from .models import Section, SectionEvent, Student, PEvent


# Register your models here.


admin.site.register(Section)
admin.site.register(Student)
admin.site.register(SectionEvent)
admin.site.register(PEvent)
