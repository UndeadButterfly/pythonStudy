from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

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
    # logging.info('page:{}'.format(page))

    question_list = Question.objects.order_by('-create_date')  # order_by('-필드') desc,order_by('필드') asc
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
    context = {'question_list': page_obj}
    # logging.info('question_list:{}'.format(question_list))
    return render(request, 'pybo/question_list.html', context)
