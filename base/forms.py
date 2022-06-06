from django.forms import ModelForm
from django import forms
from .models import Section, SectionEvent, Student, PEvent
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['college', 'branch', 'section']


class SectionEventsForm(forms.Form, ModelForm):
    date = forms.DateField(widget=AdminDateWidget, label=(
        "Date (Only for Other Events)"), required=False)
    time = forms.TimeField(widget=AdminTimeWidget)

    class Meta:
        model = SectionEvent
        exclude = ['date', 'time', 'section']


class StudentForm(ModelForm):
    class Meta:
        model = Student
        exclude = ['student_username']
        # fields = '__all__'


class StudentEventsForm(ModelForm):
    date = forms.DateField(widget=AdminDateWidget)
    time = forms.TimeField(widget=AdminTimeWidget)

    class Meta:
        model = PEvent
        exclude = ['date', 'time', 'pevents']
