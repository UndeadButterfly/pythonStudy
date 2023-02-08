import requests
from bs4 import BeautifulSoup
from django.shortcuts import render


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
