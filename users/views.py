# coding=utf-8
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib import auth, messages
import hashlib, datetime, random
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from .models import UserProfile, User
from .forms import UserLoginForm, UserRegistrationForm, UserChangeForm


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
        "form": form,
    }
    return render(request, template, context)


def logout_view(request):
    auth.logout(request)
    return redirect("/user/login/")


def register_user(request):
    form = UserRegistrationForm(request.POST or None)
    if request.user.is_authenticated():
        return render(request, 'index.html')
    if request.method == 'POST':
        if form.is_valid():
            form.save()  # save user to database if form is valid
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            activation_key = hashlib.sha1(salt + email).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(7)

            # Get user by username
            user = User.objects.get(email=email)

            # Create and save user profile
            new_profile = UserProfile(user=user, activation_key=activation_key,
                                      key_expires=key_expires)
            new_profile.save()

            # Send email with activation key
            email_subject = 'Подтверждение регистрации'
            email_body = "Привет {}, спасибо за регистрацию. Чтобы активировать свой аккаунт нажми на ссылку ниже" \
                         "в течении 7 дней 48hours http://127.0.0.1:8000/accounts/confirm/{}" \
                .format(email, activation_key)

            send_mail(email_subject, email_body, 'kup9python@gmail.com',
                      [email], fail_silently=False)

            return redirect('/admin')
        else:
            messages.warning(request, "Form is not valid!")
            return render(request, 'users/register.html', {'form': form})
    return render(request, 'users/register.html', {'form': form})


def register_confirm(request, activation_key):
    if request.user.is_authenticated():
        return redirect('/index/')

    # Проверка сходится ли пользователь с ключем активации
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    # Проверка, не истек ли еще ключ активации
    if user_profile.key_expires:
        return render('user_profile/confirm_expired.html')
    # если ключ норм, то активировать пользователя
    user = user_profile.user
    user.is_active = True
    user.save()
    return render(request, 'user_profile/confirm.html')



class UserListView(ListView):
    model = User
    template_name = "users/user_list_view.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(UserListView, self).get_queryset(**kwargs)
        qs = qs.filter(is_active=True)
        return qs


class UserDetailView(DetailView):
    model = User
    template_name = "users/user_detail_view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetailView, self).get_context_data(*args, **kwargs)
        instance = self.get_object()
        context['instance'] = instance
        return context


def user_edit_profile(request, pk):
    user = User.objects.get(pk=pk)
    form = UserChangeForm(request.POST or None, request.FILES or None, instance=user)
    template = 'users/user_change_profile.html'
    if request.POST and form.is_valid():
        form.save()
    return render(request, template, {'form': form})






# def user_list_view(request):
#     template = "users/user_list_view.html"
#     queryset = User.objects.all().filter(is_active=True)
#     phone = request.user.get('phone')
#     print phone
#     context = {
#         'queryset': queryset,
#         'phone': phone,
#     }
#     return render(request, template, context)


