from django.db.models import Avg, Sum
from datetime import datetime, timezone
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import SignUpForm
from .models import *
from detection.models import Logs, FalseLogin
from django.contrib import messages
from detection.views import *
from django.contrib.auth import authenticate, login, logout
from django_user_agents.utils import get_user_agent
# Create your views here.


def dashboard(request):
    users = CustomUser.objects.all()

    check = Registration.objects.filter(student=request.user).exists()
    if request.user.is_authenticated:
        context = {'users': users,
                   'first': Course.objects.filter(
                       sem='1st'), 'second': Course.objects.filter(sem='2nd')}
        if not request.user.is_superuser and check:
            first = Registration.objects.filter(
                student=request.user, course__sem='1st')
            second = Registration.objects.filter(
                student=request.user, course__sem='2nd')
            f = first.aggregate(Sum('course__unit'))
            s = second.aggregate(Sum('course__unit'))
            fsum = f['course__unit__sum']
            ssum = s['course__unit__sum']
            context = {
                'first': first, 'fsum': fsum, 'ssum': ssum, 'second': second}
        context['registered'] = check
        return render(request, 'dashboard.html', context)
    else:
        return redirect(reverse('login'))


def user_logout(request):
    logout(request)
    return redirect(reverse('login'))


def user_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))

    context = {}
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user == None:
            messages.error(request, 'Invalid Credentials')
        else:
            # Valid Details Were Provided - So, we check for possible intrusion
            login(request, user)
            report = detect_intrusion(request, user)
            if report:
                FalseLogin.objects.create(user=user)
            return redirect(reverse('dashboard'))
    return render(request, 'login.html', context)


def user_register(request):
    form = SignUpForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            ip = get_client_ip(request)
            os = request.user_agent.os.family
            device = get_device(request)
            browser = request.user_agent.browser.family
            device_family = request.user_agent.device.family
            location = get_geolocation_for_ip(ip)
            if location == None:
                location = "Unknown"

            Logs.objects.create(user=user, ip=ip, device=device, os=os,
                                device_family=device_family, browser=browser, location=location,   category='R')
            messages.success(request, "Account Created")
            return redirect(reverse('login'))
        else:
            messages.error(request, "Form Errors")
    return render(request, 'register.html', context)


def fetch(request):
    objects = FalseLogin.objects.filter(seen=False)
    json_data = []
    for obj in objects:
        current_date = datetime.now(timezone.utc)
        minutes_since_created = (current_date - obj.date_created).seconds / 60
        if minutes_since_created > 2:  # More than 2 minutes, kindly block
            block(request, obj.user.id)
            data = {"id": obj.user.id, "user":  str(
                    obj.user), "date": str(obj.date_created), "auto": 1}
        else:
            data = {"id": obj.user.id, "user":  str(
                obj.user), "date": str(obj.date_created)}
        json_data.append(data)
    return JsonResponse(json.dumps(json_data), safe=False)


def block(request, id):
    user = get_object_or_404(CustomUser, id=id)
    try:
        FalseLogin.objects.filter(user=user, seen=False).update(seen=True)
    except:
        pass
    user.is_active = False
    user.save()
    return redirect(reverse('dashboard'))


def ignore(request, id):
    user = get_object_or_404(CustomUser, id=id)
    try:
        FalseLogin.objects.filter(user=user, seen=False).update(seen=True)
    except:
        pass
    return redirect(reverse('dashboard'))


def submit(request):
    student_data = request.POST.getlist('course[]')
    student = request.user
    if len(student_data) < 1:
        messages.error(request, "Please select at least one elective")
        return redirect(reverse('dashboard'))

    for data in student_data:
        course = Course.objects.get(id=data)
        reg = Registration()
        reg.student = student
        reg.course = course
        reg.save()
    student.status = True
    student.save()
    messages.success(request, "Course registration completed.")
    return redirect(reverse('dashboard'))
