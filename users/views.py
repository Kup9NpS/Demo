# coding=utf-8
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib import auth, messages


from .forms import UserLoginForm

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if request.user.is_authenticated():
        return redirect('/admin')
    if form.is_valid:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        print email, password
        user = auth.authenticate(username=email, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return redirect("/admin")
        else:
            messages.warning(request, "Пользователь не найден!")
    template = "login.html"
    context = {
        "form":form,
        }
    return render(request, template, context)


def logout_view(request):
    auth.logout(request)
    return redirect("/user/login/")