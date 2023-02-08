import requests
from bs4 import BeautifulSoup
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


def crawling_cgv(request):
    """http://www.cgv.co.kr/movies/?lt=1&ft=0"""
    url = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
    response = requests.get(url)
    context = {}
    if 200 == response.status_code:
        html = response.text
        # print('html:{}'.format(html))
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select('div.box-contents strong.title')
        percent = soup.select('strong.percent span')
        poster = soup.select('span.thumb-image img')
        title_list = []  # 제목
        percent_list = []  # 예매율
        poster_list = []  # 포스터
        print('title:{}'.format(title))
        for page in range(0, 7, 1):
            print('title[{}]:{}'.format(page, title[page].get_text()), end=", ")
            title_list.append(title[page].get_text())
            print('percent[{}]:{}'.format(page, percent[page].get_text()))
            percent_list.append(percent[page].get_text())
            print('poster[{}]:{}'.format(page, poster[page].get('src')))
            poster_list.append(poster[page].get('src'))
        context = {'context': zip(title_list, percent_list, poster_list)}
    else:
        print('접속 오류 response.status_code:{}'.format(response.status_code))
    return render(request, 'pybo/crawling_cgv.html', context)
