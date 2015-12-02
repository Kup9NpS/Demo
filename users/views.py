# coding=utf-8
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib import auth, messages
import hashlib, datetime, random

from .models import UserProfile, Activation
from .forms import UserLoginForm, UserRegistrationForm

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
    template = "users/login.html"
    context = {
        "form":form,
        }
    return render(request, template, context)


def logout_view(request):
    auth.logout(request)
    return redirect("/user/login/")


def register_user(request):
    if request.user.is_authenticated():
        return render(request, 'index.html')
    context = {}
    context.update(csrf(request))
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        context['form'] = form
        if form.is_valid():
            form.save() # save user to database if form is valid
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt+email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(7)

            #Get user by username
            user=User.objects.get(pk=1)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Подтверждение регистрации'
            email_body = "Привет %s, спасибо за регистрацию. Чтобы активировать свой аккаунт нажми на ссылку ниже" \
                         " в течении 7 дней 48hours http://127.0.0.1:8082/accounts/confirm/%s" \
                         % (username, activation_key)

            send_mail(email_subject, email_body, 'myemail@example.com',
                        [email], fail_silently=False)

            return redirect('/admin')
        else:
            context['form'] = form
            messages.success(request, "Form is not valid!")
            return (request,'users/register.html', context)
    context['form'] = UserRegistrationForm()
    return render(request,'users/register.html', context)

#
# def register_confirm(request, activation_key):
#     # check if user is already logged in and if he is redirect him to some other url, e.g. home
#     if request.user.is_authenticated():
#         HttpResponseRedirect('/home')
#
#     # check if there is UserProfile which matches the activation key (if not then display 404)
#     user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
#
#     # check if the activation key has expired, if it hase then render confirm_expired.html
#     if user_profile.key_expires:
#         return render_to_response('user_profile/confirm_expired.html')
#     # if the key hasn't expired save user and set him as active and render some template to confirm activation
#     user = user_profile.user
#     user.is_active = True
#     user.save()
#     return render_to_response('user_profile/confirm.html')