from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from pybo.models import Question


# Create your views here.
def detail(request, question_id):
    """question 상세"""
    # logging.info('1.question_id:{}'.format(question_id))
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    # logging.info('2.question:{}'.format(question))
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def index(request):
    """question list"""
    # list order create_date desc
    # logging.info('index 레벨로 출력')

    # 입력인자
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')
    # logging.info('page:{}'.format(page))

    question_list = Question.objects.order_by('-create_date')  # order_by('-필드') desc,order_by('필드') asc
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw) |  # 내용 검색
            Q(answer__content__icontains=kw) |  # 답변 내용 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()
    # paging
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    # paginator.count : 전체 게시물 개수
    # paginator.per_page : 페이지 당 보여줄 게시물 개수
    # paginator.page_range : 페이지 범위
    # has_next
    # has_previous
    # has_other_pages
    # next_page_number
    # previous_page_number
    # start_index
    # end_index
    # question_list = Question.objects.filter(id=99)
    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    # logging.info('question_list:{}'.format(question_list))
    return render(request, 'pybo/question_list.html', context)
