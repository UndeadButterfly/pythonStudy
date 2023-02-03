from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils import timezone
from .models import Question
from .forms import QuestionForm, AnswerForm
import logging
import requests
from bs4 import BeautifulSoup


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


def answer_create(request, question_id):
    """답변등록"""
    logging.info('answer_create question_id:{}'.format(question_id))
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.create_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        return HttpResponseNotAllowed('Post만 가능합니다.')

    # form validation
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)
    # Question 과 Answer 처럼 서로 연결되어 있는 경우
    # 연결모델명_set 연결데이터를 조회할 수 있다.


def question_create(request):
    """질문등록"""

    logging.info('1.request.method:{}'.format(request.method))
    if request.method == 'POST':
        logging.info('2.question_create post')
        # 저장
        form = QuestionForm(request.POST)  # request.POST 데이터(subject, content 자동 생성)
        logging.info('3.question_create post')
        # form(질문등록)이 유효하면
        if form.is_valid():
            logging.info('4.form.is_valid():{}'.format(form.is_valid()))
            question = form.save(commit=False)  # subject, content 만 저장(commit 은 하지 않음)
            question.create_date = timezone.now()
            question.save()  # 날짜까지 생성해서 저장(Commit)
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


def detail(request, question_id):
    """question 상세"""
    logging.info('1.question_id:{}'.format(question_id))
    # question = Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    logging.info('2.question:{}'.format(question))
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


def index(request):
    """question list"""
    # list order create_date desc
    logging.info('index 레벨로 출력')
    question_list = Question.objects.order_by('-create_date')  # order_by('-필드') desc,order_by('필드') asc
    # question_list = Question.objects.filter(id=99)
    context = {'question_list': question_list}
    logging.info('question_list:{}'.format(question_list))
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
