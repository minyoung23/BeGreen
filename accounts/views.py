from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm

def register(request):

    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user':new_user})
    else:
        user_form = RegisterForm()

    return render(request, 'registration/register.html',{'form':user_form})

def ForgotIDview(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            if user is not None:
                    messages.info(request, str(user.username))
        except:
            messages.info(request, "존재하지 않는 회원입니다.")
    context = {}
    return render(request, 'registration/forgot_id.html', context)

#회원정보 수정
from .forms import CustomUserChangeForm
from django.contrib.auth.decorators import login_required


def change(request):
    return render(request, 'registration/update.html')

@login_required
@require_http_methods(['GET','POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'registration/update.html')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'registration/change.html', {'form':form})

@login_required
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return render(request, 'registration/login.html')
    return render(request, 'registration/delete.html')


#비밀번호 변경 폼
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            # 추가된 부분
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            return render(request, 'registration/login.html')
    else:
        password_change_form = PasswordChangeForm(request.user)
    return render(request, 'registration/password.html', {'password_change_form': password_change_form})
