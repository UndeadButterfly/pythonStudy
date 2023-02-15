"""
파일명 : urls.py
설 명 : board urls
생성일 : 2023-02-15
생성자 : highprime
since 2023.01.09 Copyright (C) by KandJang All right reserved.
"""
from django.urls import path

from . import views

app_name = 'board'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='board_create'),
    path('<int:board_id>/', views.detail, name='board_detail'),
    path('modify/<int:board_id>/', views.modify, name='board_modify'),
    path('delete/<int:board_id>/', views.delete, name='board_delete'),
]
