from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm
from .models import PEvent, Section, SectionEvent, Student
from .forms import SectionForm, StudentForm
from itertools import chain


def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {'page': page}
    return render(request, "base/login.html", context)


@login_required(login_url='login_user')
def logoutUser(request):
    logout(request)
    return redirect('login_user')


def registeruser(request):
    page = 'signup'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('register')
        else:
            messages.error(request, 'An error occurred during signup')
    form = UserCreationForm()
    context = {'form': form, 'page': page}
    return render(request, 'base/login.html', context)


@login_required(login_url='login_user')
def registerstudent(request):
    page = 'student-creation'
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            studentobj = Student.objects.create(
                student_username=request.user.username,
                student_name=data.get('student_name'),
                student_section=data.get('student_section'),
                student_rollno=data.get('student_rollno')
            )
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    form = StudentForm()
    context = {'form': form, 'page': page}
    return render(request, 'base/login.html', context)


def home(request):
    try:
        if request.user.is_authenticated:
            student = Student.objects.get(
                student_username=request.user.username)
            section = Section.objects.get(id=student.student_section.id)
            today = section.sectionevent_set.all().filter(
                name=str(datetime.today().weekday()+1))
            mon = section.sectionevent_set.all().filter(name='1').order_by('time')
            tue = section.sectionevent_set.all().filter(name='2').order_by('time')
            wed = section.sectionevent_set.all().filter(name='3').order_by('time')
            thu = section.sectionevent_set.all().filter(name='4').order_by('time')
            fri = section.sectionevent_set.all().filter(name='5').order_by('time')
            sat = section.sectionevent_set.all().filter(name='6').order_by('time')
            sun = section.sectionevent_set.all().filter(name='7').order_by('time')
            Deleter(section.sectionevent_set.all().filter(name='8'))
            other = section.sectionevent_set.all().filter(
                name='8').order_by('date')
            Deleter(student.pevent_set.all())
            studentpersonal = student.pevent_set.all().order_by('dateTime')
            today = sorted(chain(today, studentpersonal.filter(date=datetime.now().date()), other.filter(date=datetime.now().date())),
                           key=lambda instance: instance.time)

            context = {'section': section, 'student': student, 'today': today, 'mon': mon, 'tue': tue, 'wed': wed, 'thu': thu,
                       'fri': fri, 'sat': sat, 'sun': sun, 'other': other, 'studentpersonal': studentpersonal}
            return render(request, 'base/home.html', context)
        else:
            return redirect('login_user')
    except:
        return redirect('register')


@login_required(login_url='login_user')
def getSectionEvents(request, pk):
    page = 'se'
    student = Student.objects.get(id=pk)
    section = Section.objects.get(id=student.student_section.id)

    if request.user.username != student.student_username:
        messages.error(request, 'You are not allowed there!!')
        return redirect('home')

    if request.method == 'POST':
        SectionEvent.objects.create(
            section=section,
            name=request.POST.get('name'),
            event_name=request.POST.get('event_name'),
            date=None if request.POST.get(
                'date') == '' else request.POST.get('date'),
            time=Tconverter(request.POST.get('time'))
        )
        return redirect('section-events', pk=student.id)
    mon = section.sectionevent_set.all().filter(name='1').order_by('time')
    tue = section.sectionevent_set.all().filter(name='2').order_by('time')
    wed = section.sectionevent_set.all().filter(name='3').order_by('time')
    thu = section.sectionevent_set.all().filter(name='4').order_by('time')
    fri = section.sectionevent_set.all().filter(name='5').order_by('time')
    sat = section.sectionevent_set.all().filter(name='6').order_by('time')
    sun = section.sectionevent_set.all().filter(name='7').order_by('time')
    other = section.sectionevent_set.all().filter(name='8').order_by('date')
    context = {'section': section, 'student': student, 'page': page,  'mon': mon, 'tue': tue, 'wed': wed, 'thu': thu,
               'fri': fri, 'sat': sat, 'sun': sun, 'other': other}
    return render(request, 'base/seforms.html', context)


@login_required(login_url='login_user')
def studentdetails(request, pk):
    student = Student.objects.get(id=pk)
    section = Section.objects.get(id=student.student_section.id)
    sections = Section.objects.all()

    if request.user.username != student.student_username:
        messages.error(request, 'You are not allowed there!!')
        return redirect('home')

    if request.method == 'POST':
        student.student_section = Section.objects.get(
            id=request.POST.get('sect'))
        student.student_name = request.POST.get('name')
        student.student_rollno = request.POST.get('rollno')
        student.save()
        return redirect('home')

    context = {'section': section,
               'sections': sections, 'student': student}
    return render(request, 'base/edituserform.html', context)


@login_required(login_url='login_user')
def studentpersonalevents(request, pk):
    student = Student.objects.get(id=pk)
    section = Section.objects.get(id=student.student_section.id)

    if request.user.username != student.student_username:
        messages.error(request, 'You are not allowed there!!')
        return redirect('home')

    if request.method == 'POST':
        pevent = PEvent.objects.create(
            pevents=student,
            event_name=request.POST.get('event_name'),
            date=request.POST.get('date'),
            time=Tconverter(request.POST.get('time'))
        )
        pevent.dateTime = DTconverter(pevent.time, pevent.date)
        pevent.save()
        return redirect('student-events', pk=student.id)

    studentpersonal = student.pevent_set.all()
    context = {'section': section, 'student': student,
               'studentpersonal': studentpersonal}
    return render(request, 'base/peform.html', context)


@login_required(login_url='login_user')
def changep(request):
    student = Student.objects.get(student_username=request.user.username)
    section = Section.objects.get(id=student.student_section.id)

    if request.method == 'POST':
        user = request.user
        if user.check_password(request.POST.get('old-p')) and request.POST.get('new-p') == request.POST.get('new-p-c'):
            user.set_password(request.POST.get('new-p'))
            user.save()
            update_session_auth_hash(request, user)
        return redirect('home')

    context = {'section': section, 'student': student}
    return render(request, 'base/updatepass.html', context)


def cs(request):
    form = SectionForm()
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register')

    context = {'form': form}
    return render(request, 'base/createsection.html', context)


@login_required(login_url='login_user')
def deleteevents(request, pk, pk2):
    if not request.user.is_staff:
        messages.error(request, 'You are not allowed there!!')
        return redirect('home')
    try:
        sectionevent = SectionEvent.objects.get(id=pk2)
        sectionevent.delete()
        return redirect('section-events', pk)
    except:
        messages.error(request, 'Item doesnot exist')
        return redirect('home')


@login_required(login_url='login_user')
def deleteeventp(request, pk, pk2):
    try:
        pevent = PEvent.objects.get(id=pk2)
        pevent.delete()
        return redirect('student-events', pk)
    except:
        messages.error(request, 'Item doesnot exist')
        return redirect('home')


def Tconverter(time):
    hour = time[0:2]
    minutes = time[3:5]
    temp = time[6:8]

    if temp == 'am':
        return hour + ':' + minutes + ':00'

    elif temp == 'pm':
        hour = str(int(hour)+12)
        return hour + ':' + minutes + ':00'


def DTconverter(time, date):
    # time = Tconverter(time)
    return datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]),
                    int(time[0:2]), int(time[3:5]), int(time[6:8]))
    # 16:00:00 2022-06-03


def Deleter(events):
    for event in events:
        if event.date < datetime.now().date():
            event.delete()
