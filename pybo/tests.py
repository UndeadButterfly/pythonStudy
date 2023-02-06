import logging

from django.test import TestCase

# Create your tests here.
import unittest
import datetime
import logging
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pyperclip  # 클립보드를 쉽게 활용할 수 있게 해주는 모듈
from selenium.webdriver.common.keys import Keys


class Crawling(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(executable_path='C:/BIG_AI0102/01_PYTHON/app/geckodriver.exe')
        print('setUp')

    def tearDown(self):
        print('tearDown')
        # self.browser.quit()

    def test_clipboard_naver(self):
        """clipboard 를 통한 naver login"""
        self.browser.get("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")
        user_id = 'highprime'
        user_pw = 'fkdlzj28'

        # id
        id_textinput = self.browser.find_element(By.ID, 'id')
        id_textinput.click()
        # 클립보드로 copy
        pyperclip.copy(user_id)
        id_textinput.send_keys(Keys.CONTROL, 'v')  # 클립보드에서 id_textinput 으로 copy
        time.sleep(1)

        # password
        pw_textinput = self.browser.find_element(By.ID, 'pw')
        pw_textinput.click()
        # 클립보드로 copy
        pyperclip.copy(user_pw)
        pw_textinput.send_keys(Keys.CONTROL, 'v')  # 클립보드에서 id_textinput 으로 copy
        time.sleep(1)

        #로그인 버튼
        btn_login = self.browser.find_element(By.ID, 'log.login')
        btn_login.click()

        pass

    @unittest.skip('')
    def test_selenium(self):
        # FireFoxz 웹 드라이버 객체에게 Get을 통하여 네이버의 http 요청을 하게 함
        self.browser.get('http://127.0.0.1:8000/pybo/3/')
        print(self.browser.title)
        self.assertIn('Pybo', self.browser.title)

        content_textarea = self.browser.find_element(By.ID, 'content')
        content_textarea.send_keys('오늘은 안 즐거운 금요일!')

        btn = self.browser.find_element(By.ID, 'submit_btn')
        btn.click()  # 버튼 클릭
        pass

    @unittest.skip('naver login')
    def test_naver(self):
        self.browser.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')

        id_textarea = self.browser.find_element(By.ID, 'id')
        id_textarea.send_keys('highprime')
        pw_textarea = self.browser.find_element(By.ID, 'pw')
        pw_textarea.send_keys('fkdlzj28')

        btn = self.browser.find_element(By.ID, 'log.login')
        btn.click()  # 버튼 클릭
        pass

    @unittest.skip('')
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
