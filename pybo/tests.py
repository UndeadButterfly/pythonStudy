import logging

from django.test import TestCase

# Create your tests here.
import unittest
import datetime
import logging
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen


class Crawling(unittest.TestCase):
    def setUp(self):
        print('setUp')

    def tearDown(self):
        print('tearDown')

    def test_zip(self):
        integers = [1, 2, 3]
        letters = ['a', 'b', 'c']
        floats = [4.0, 8.0, 10.0]
        zipped = zip(integers, letters, floats)
        list_data = list(zipped)
        print(list_data)
        pass

    @unittest.skip('naver stock')
    def test_naver_stock(self):
        """주식 크롤링"""
        for code in ["005930", "005380"]:
            url = 'https://finance.naver.com/item/main.naver?code=' + code
            response = requests.get(url)
            if 200 == response.status_code:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                stock_price = soup.select('div.today span.blind:first-child')
                print(stock_price[0].text)
            else:
                print('접속 오류 response.status_code:{}'.format(response.status_code))

    @unittest.skip('slamdunk reviews')
    def test_slamdunk(self):
        # https://movie.naver.com/movie/point/af/list.naver?st=mcode&sword=223800&target=after&page=1
        for page_num in range(1, 4, 1):
            url = "https://movie.naver.com/movie/point/af/list.naver?st=mcode&sword=223800&target=after&page=" + str(
                page_num)
            response = requests.get(url)
            if 200 == response.status_code:
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                ac_num = soup.select('table.list_netizen tbody tr td.ac')
                title = soup.select('table.list_netizen tbody tr td.title')
                score = soup.select('div.list_netizen_score em')
                author = soup.select('table.list_netizen tbody tr td.num a.author')
                author_date = soup.select('table.list_netizen tbody tr td.num:last-child ')
                for no in range(0, 10, 1):
                    print('번호 :', ac_num[no].text)
                    print('-' * 50)
                    print('별점 :', score[no].text)
                    print(title[no].text.split('\n')[5])
                    print('-' * 50)
                    print('글쓴이 :', author[no].text)
                    print('-' * 50)
                    print('날짜 :', author_date[no].text.strip(author[no].text))
                    print('=' * 50)
            else:
                print('접속 오류 response.status_code:{}'.format(response.status_code))

    @unittest.skip('')
    def test_cgv(self):
        """http://www.cgv.co.kr/movies/?lt=1&ft=0"""
        url = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
        response = requests.get(url)
        if 200 == response.status_code:
            html = response.text
            # print('html:{}'.format(html))
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.select('div.box-contents strong.title')
            percent = soup.select('strong.percent span')
            open_date = soup.select('span.txt-info strong')
            poster = soup.select('span.thumb-image img')
            print('title:{}'.format(title))
            for page in range(0, 7, 1):
                print('title[{}]:{}'.format(page, title[page].get_text()), end=", ")
                print('percent[{}]:{}'.format(page, percent[page].get_text()))
                print('poster[{}]:{}'.format(page, poster[page].get_attribute_list('src')[0]))
                print('poster[{}]:{}'.format(page, poster[page].get('src')))
                print('poster[{}]:{}'.format(page, poster[page].attrs['src']))
                pass

        else:
            print('접속 오류 response.status_code:{}'.format(response.status_code))

    @unittest.skip('테스트 연습')
    def test_weather(self):
        """날씨"""
        # https://weather.naver.com/
        now = datetime.datetime.now()
        # yyyymmdd HH:MM
        new_date = now.strftime('%Y-%m-%d, %H:%M:%S')
        print('=' * 35)
        print(new_date)
        print('=' * 35)
        naver_weather_url = 'https://weather.naver.com/'
        html = urlopen(naver_weather_url)
        # print('html:{}'.format(html))
        bs_object = BeautifulSoup(html, 'html.parser')
        tmpes = bs_object.find('strong', 'current')
        print('서울 마포구 서교동 날씨:{}'.format(tmps.get_text()))
        print('test_weather')
        pass
