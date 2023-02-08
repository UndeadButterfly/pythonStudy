import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from pybo.forms import QuestionForm
from pybo.models import Question


# Create your views here.


def boot_menu(request):
    """개발에 사용되는 임시메뉴"""
    return render(request, 'pybo/menu.html')


def boot_reg(request):
    return render(request, 'pybo/reg.html')


# bootstrap list
def boot_list(request):
    """bootstrap template"""
    return render(request, 'pybo/list.html')


@login_required(login_url='common:login')
def question_create(request):
    """질문등록"""

    # logging.info('1.request.method:{}'.format(request.method))
    if request.method == 'POST':
        # logging.info('2.question_create post')
        # 저장
        form = QuestionForm(request.POST)  # request.POST 데이터(subject, content 자동 생성)
        # logging.info('3.question_create post')
        # form(질문등록)이 유효하면
        if form.is_valid():
            # logging.info('4.form.is_valid():{}'.format(form.is_valid()))
            question = form.save(commit=False)  # subject, content 만 저장(commit 은 하지 않음)
            question.create_date = timezone.now()
            question.author = request.user
            question.save()  # 날짜까지 생성해서 저장(Commit)
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            logging.info(question.id)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)
