"""
파일명 : pybo_filter.py
설 명 : 빼기 필터
생성일 : 2023-02-03
생성자 : highprime
since 2023.01.09 Copyright (C) by KandJang All right reserved.
"""
import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def sub(value, arg):
    """
    @register.filter : 템플릿에서 필터로 사용할 수 있게 된다.
    빼기 필터
    """
    return value - arg


@register.filter
def mark(value):
    """입력된 문자열을 html 로 변환"""
    # nl2br(줄바꿈문자 -> <br>, fenced_code(마크다운))
    # nl2br 마크다운에서 줄바꿈은 스페이스를 두개 연속 입력해야 한다.
    extensions = ['nl2br', 'fenced_code']
    return mark_safe(markdown.markdown(value, extensions=extensions))
