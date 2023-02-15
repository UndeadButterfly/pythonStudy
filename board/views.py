import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from board.forms import BoardForm
from board.models import Board


# Create your views here.
def index(request):
    # 입력인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')
    div = request.GET.get('div', '')
    per_page = request.GET.get('per_page', '10')
    # logging.info('page:{}'.format(page))

    board_list = Board.objects.order_by('-create_date')  # order_by('-필드') desc,order_by('필드') asc
    if kw:
        if div == '10':
            board_list = board_list.filter(
                Q(subject__icontains=kw)  # 제목 검색
            ).distinct()
        elif div == '20':
            board_list = board_list.filter(
                Q(content__icontains=kw)  # 내용 검색
            ).distinct()
        elif div == '30':
            board_list = board_list.filter(
                Q(author__username__icontains=kw)  # 작성자 검색
            ).distinct()
        else:
            board_list = board_list.filter(
                Q(subject__icontains=kw) |  # 제목 검색
                Q(content__icontains=kw) |  # 내용 검색
                Q(author__username__icontains=kw)  # 질문 글쓴이 검색
            ).distinct()
    # paging
    paginator = Paginator(board_list, per_page)
    page_obj = paginator.get_page(page)

    context = {'board_list': page_obj, 'page': page, 'kw': kw, 'div': div, 'per_page': per_page}
    # logging.info('question_list:{}'.format(question_list))
    return render(request, 'board/board_list.html', context)


def detail(request, board_id):
    """question 상세"""
    # logging.info('1.question_id:{}'.format(question_id))
    # question = Question.objects.get(id=question_id)
    board = get_object_or_404(Board, pk=board_id)
    # logging.info('2.question:{}'.format(question))
    context = {'board': board}
    return render(request, 'board/board_detail.html', context)


@login_required(login_url='common:login')
def create(request):
    """게시판등록"""

    if request.method == 'POST':
        # 저장
        form = BoardForm(request.POST)  # request.POST 데이터(subject, content 자동 생성)
        # logging.info('3.question_create post')
        # form(질문등록)이 유효하면
        if form.is_valid():
            # logging.info('4.form.is_valid():{}'.format(form.is_valid()))
            board = form.save(commit=False)  # subject, content 만 저장(commit 은 하지 않음)
            board.create_date = timezone.now()
            board.author = request.user
            board.save()  # 날짜까지 생성해서 저장(Commit)
            return redirect('board:index')
    else:
        form = BoardForm()
    context = {'form': form}
    return render(request, 'board/board_form.html', context)


@login_required(login_url='common:login')
def modify(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:board_detail', board_id=board.id)
    if request.method == "POST":
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            logging.info(board.id)
            board.modify_date = timezone.now()
            board.save()
            return redirect('board:board_detail', board_id=board.id)
    else:
        form = BoardForm(instance=board)
    context = {'form': form}
    return render(request, 'board/board_form.html', context)


@login_required(login_url='common:login')
def delete(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board:board_detail', board_id=board.id)
    board.delete()
    return redirect('board:index')
