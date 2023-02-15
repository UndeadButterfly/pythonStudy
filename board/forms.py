"""
파일명 : forms.py
설 명 :
생성일 : 2023-02-15
생성자 : highprime
since 2023.01.09 Copyright (C) by KandJang All right reserved.
"""
from django import forms

from board.models import Board


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board  # 사용할 Question model
        fields = ['subject', 'content']  # BoardForm 사용할 board model 의 속성
        widgets = {
            # class = "form-control"
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'subject': '제목',
            'content': '내용',
        }
