#! python3
# coding=utf-8


import NetUtils
import bs4
from bs4 import BeautifulSoup
import WordsSplitUtils
import TimeUtils


class EasyMoneyUtils:

    # http://finance.eastmoney.com/news/cgnjj.html
    @staticmethod
    def get_economic_china_news(url):
        resp = NetUtils.NetUtils.request(url)
        html = NetUtils.NetUtils.decode(resp['data'], 'utf-8')
        soup = BeautifulSoup(html, 'lxml')
        news_raw_list = soup.select('#ContentBody > p')
        news = ''
        for news_raw in news_raw_list:
            children_iterator = news_raw.descendants
            for child in children_iterator:
                if bs4.element.NavigableString == type(child):
                    news += child
            news = news.strip()
            news = '{}\r\n'.format(news)

        words_split_handler = WordsSplitUtils.WordsSplitHandler(data=news, analyse_type=WordsSplitUtils.type_jieba)
        words_split_handler.get_split_words()
        return words_split_handler.simplify()

    @staticmethod
    def _get_economic_china_news_url_list_with_page_datetime(page_list, datetime_list, datetime_pattern):
        url_list = list()
        for page in page_list:
            if page > 0:
                if 1 == page:
                    url = 'http://finance.eastmoney.com/news/cgnjj.html'
                else:
                    url = 'http://finance.eastmoney.com/news/cgnjj_{}.html'.format(page)
                news_list_html_raw = NetUtils.NetUtils.request(url)
                news_list_html = NetUtils.NetUtils.decode(news_list_html_raw['data'], 'utf-8')
                soup = BeautifulSoup(news_list_html, 'lxml')
                news_list_raw = soup.select('#newsListContent > li')
                for news_raw in news_list_raw:
                    # 获取新闻发布日期
                    time_str = news_raw.find('p', 'time').get_text().strip()
                    date_time = TimeUtils.TimeUtils.str_2_datetime(time_str, '%m月%d日 %H:%M')
                    date_time = TimeUtils.TimeUtils.replace_year(date_time,  # 从1900年转为今年
                                                                 TimeUtils.TimeUtils.get_today_datetime().year)
                    # 判断时间是否在datetime_list内
                    datetime_range_list = TimeUtils.TimeUtils.get_datetime_range(datetime_list, datetime_pattern)
                    in_range = False
                    for datetime_range in datetime_range_list:
                        if datetime_range[0] <= date_time <= datetime_range[1]:
                            in_range = True
                            break
                    if in_range is True:
                        url_list.append(news_raw.find('a')['href'])
                TimeUtils.TimeUtils.sleep(1000)
        return url_list

    @staticmethod
    def _get_economic_china_news_url_list_with_datetime(datetime_list, datetime_pattern):
        url_list = list()
        page_list = range(1, 26)  # 从网页上看页数范围是第1页-第25页，如果以后发现有不同的再进行改进
        do_last_datetime_range = False
        for page in page_list:
            if page > 0:
                if 1 == page:
                    url = 'http://finance.eastmoney.com/news/cgnjj.html'
                else:
                    url = 'http://finance.eastmoney.com/news/cgnjj_{}.html'.format(page)
                news_list_html_raw = NetUtils.NetUtils.request(url)
                news_list_html = NetUtils.NetUtils.decode(news_list_html_raw['data'], 'utf-8')
                soup = BeautifulSoup(news_list_html, 'lxml')
                news_list_raw = soup.select('#newsListContent > li')
                for news_raw in news_list_raw:
                    # 获取新闻发布日期
                    time_str = news_raw.find('p', 'time').get_text().strip()
                    date_time = TimeUtils.TimeUtils.str_2_datetime(time_str, '%m月%d日 %H:%M')
                    date_time = TimeUtils.TimeUtils.replace_year(date_time,  # 从1900年转为今年
                                                                 TimeUtils.TimeUtils.get_today_datetime().year)
                    # 判断时间是否在datetime_list内
                    datetime_range_list = TimeUtils.TimeUtils.get_datetime_range(datetime_list, datetime_pattern)
                    in_range = False
                    for datetime_range in datetime_range_list:
                        if datetime_range[0] <= date_time <= datetime_range[1]:
                            in_range = True
                            break
                    if in_range is True:
                        url_list.append(news_raw.find('a')['href'])
                    else:
                        do_last_datetime_range = True
                        break
                if do_last_datetime_range is True:
                    break
                else:
                    TimeUtils.TimeUtils.sleep(1000)
        return url_list

    @staticmethod
    def _get_economic_china_news_url_list_with_page(page_list):
        url_list = list()
        for page in page_list:
            if page > 0:
                if 1 == page:
                    url = 'http://finance.eastmoney.com/news/cgnjj.html'
                else:
                    url = 'http://finance.eastmoney.com/news/cgnjj_{}.html'.format(page)
                news_list_html_raw = NetUtils.NetUtils.request(url)
                news_list_html = NetUtils.NetUtils.decode(news_list_html_raw['data'], 'utf-8')
                soup = BeautifulSoup(news_list_html, 'lxml')
                news_list_raw = soup.select('#newsListContent > li')
                for news_raw in news_list_raw:
                    url_list.append(news_raw.find('a')['href'])
                TimeUtils.TimeUtils.sleep(1000)
        return url_list

    @staticmethod
    def get_economic_china_news_url_list(page_list=None, datetime_list=None, datetime_pattern='%Y-%m-%d'):
        news_urls_list = list()
        if page_list is not None and datetime_list is not None:
            news_urls_list = EasyMoneyUtils.\
                _get_economic_china_news_url_list_with_page_datetime(page_list, datetime_list, datetime_pattern)
        elif page_list is None and datetime_list is not None:
            news_urls_list = EasyMoneyUtils.\
                _get_economic_china_news_url_list_with_datetime(datetime_list, datetime_pattern)
        elif page_list is not None and datetime_list is None:
            news_urls_list = EasyMoneyUtils._get_economic_china_news_url_list_with_page(page_list)
        return news_urls_list

    @staticmethod
    def get_economic_china_today_news_url_list():
        return EasyMoneyUtils.get_economic_china_news_url_list(datetime_list=['2019-05-26'])
