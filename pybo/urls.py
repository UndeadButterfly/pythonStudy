"""
파일명 : urls.py
설 명 : pybo 모든 URL 과 view 함수의 매핑 담당
생성일 : 2023-01-25
생성자 : highprime
since 2023.01.09 Copyright (C) by KandJang All right reserved.
"""
from django.urls import path
from . import views  # 현재 디렉토리의 views 모듈
from .views import base_views, question_views, answer_views

app_name = 'pybo'
urlpatterns = [
    # base_views.py
    path('', base_views.index, name='index'),  # views index 로 매핑
    path('<int:question_id>/', base_views.detail, name='detail'),
    # temp menu
    path('boot/menu', base_views.boot_menu, name='boot_menu'),
    # bootstrap template
    path('boot/list/', base_views.boot_list, name='boot_list'),
    path('boot/reg/', base_views.boot_reg, name='boot_reg'),
    # crawling
    path('crawling/cgv/', base_views.crawling_cgv, name='crawling_cgv'),

    # question_views.py
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),
    path('question/vote/<int:question_id>/', question_views.question_vote, name='question_vote'),

    # answer_views.py
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
    path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),

]
