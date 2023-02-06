import logging

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from common.forms import UserForm


# Create your views here.
def signup(request):
    """회원가입"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():  # post 방식에서 form 이 유효한 경우
            # 회원가입
            form.save()
            # form username, password1
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)

            # 로그인
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
