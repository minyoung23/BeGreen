from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .forms import RegisterForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = RegisterForm()

    return render(request, 'registration/register.html', {'form': user_form})


def ForgotIDview(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            if user is not None:
                    messages.info(request, str(user.username))
        except:
            messages.info(request, "존재하지 않는 회원입니다!!")
    context = {}
    return render(request, 'registration/forgot_id.html', context)
