#! python3
# coding=utf-8


import NetUtils
import bs4
from bs4 import BeautifulSoup
import WordsSplitUtils


class EasyMoneyUtils:

    # http://finance.eastmoney.com/news/cgnjj.html
    @staticmethod
    def get_economic_china_news(url):
        resp = NetUtils.NetUtils.request(url)
        html = NetUtils.NetUtils.decode(resp['data'], 'utf-8')
        soup = BeautifulSoup(html, 'lxml')
        news_raw = soup.select('#ContentBody > p')
        children_iterator = news_raw[0].descendants
        news = ''
        for child in children_iterator:
            if bs4.element.NavigableString == type(child):
                news += child
        news = news.strip()

        words_split_handler = WordsSplitUtils.WordsSplitHandler(data=news, analyse_type=WordsSplitUtils.type_jieba)
        words_split_handler.get_split_words()
        return words_split_handler.simplify()
