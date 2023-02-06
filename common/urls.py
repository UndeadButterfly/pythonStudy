"""
파일명 : urls.py
설 명 :
생성일 : 2023-02-06
생성자 : highprime
since 2023.01.09 Copyright (C) by KandJang All right reserved.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'
urlpatterns = [
    # django.contrib.auth 앱의 LoginView 클래스를 활용
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
]
