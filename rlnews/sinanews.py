# -*- coding: utf-8 -*-

"""
新浪新闻数据接口
"""

import re
import json
import random
import lxml.html
import lxml.etree
import pandas as pd
from datetime import datetime

from rlnews import sina_constants as cts
from rlnews.utils.downloader import Downloader
from rlnews.utils.disk_cache import DiskCache

no_cache_downloader = Downloader(cache=None)
disk_cache_downloader = Downloader(cache=DiskCache())


def get_rolling_news_csv(top=50, get_content=True, classify=None, path=None):
    """
    获取新浪滚动新闻并保存成csv文件
    :param top: int, 获取的滚动新闻条数，默认为50
    :param get_content: bool, 是否获取新闻内容，默认为True
    :param classify: str, 获取的滚动新闻的类别，默认为None，即"2509:全部"
    :param path: str, 文件保存路径
    """
    try:
        df = get_rolling_news(top=top, get_content=get_content, classify=classify)
        if not path:
            path = 'news.csv'
        df.to_csv(path, index=False, encoding='utf-8')
    except Exception as e:
        print('get_rolling_news_csv error', e)
        exit(1)


def get_rolling_news(top=50, get_content=True, classify=None):
    """
    获取新浪滚动新闻
    :param top: int, 获取的滚动新闻条数，默认为50
    :param get_content: bool, 是否获取新闻内容，默认为True
    :param classify: str, 获取的滚动新闻的类别，默认为None，即"2509:全部"
    :return: pd.DataFrame, 新闻信息数据框
    """
    try:
        if classify and (classify not in cts.classifications):
            print('please set the parameter classify to be one of {}'.format(cts.classifications))
            exit(1)
        lid = cts.classification2lid.get(classify, '2509')
        classify = cts.lid2classification[lid]
        num_list = [cts.max_num_per_page] * (top // cts.max_num_per_page)
        last_page_num = top % cts.max_num_per_page
        if last_page_num:
            num_list += [last_page_num]

        df_data = []
        for page, num in enumerate(num_list, start=1):
            r = random.random()
            url = cts.template_url.format(lid, num, page, r)
            response = no_cache_downloader(url)
            response_dict = json.loads(response)
            data_list = response_dict['result']['data']

            for data in data_list:
                ctime = datetime.fromtimestamp(int(data['ctime']))
                ctime = datetime.strftime(ctime, '%Y-%m-%d %H:%M')
                url = data['url']
                row = [classify, data['title'], ctime,
                       url, data['wapurl'], data['media_name'], data['keywords']]
                if get_content:
                    row.append(get_news_content(url))
                df_data.append(row)
        df = pd.DataFrame(df_data, columns=cts.columns if get_content else cts.columns[:-1])
        return df
    except Exception as e:
        print('get_rolling_news error', e)
        exit(1)


def get_news_content(url):
    """
    获取新闻内容
    :param url: str, 新闻链接
    :return: str, 新闻内容
    """
    content = ''
    try:
        text = disk_cache_downloader(url)
        html = lxml.etree.HTML(text)
        res = html.xpath('//*[@id="artibody" or @id="article"]//p')
        p_str_list = [lxml.etree.tostring(node).decode('utf-8') for node in res]
        p_str = ''.join(p_str_list)
        html_content = lxml.html.fromstring(p_str)
        content = html_content.text_content()
        # 清理未知字符和空白字符
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'[ \xa0?]+', ' ', content)
        content = re.sub(r'\s*\n\s*', '\n', content)
        content = re.sub(r'\s*(\s)', r'\1', content)
        content = content.strip()
    except Exception as e:
        print('get_news_content(%s) error' % url, e)
    return content


if __name__ == '__main__':
    get_rolling_news_csv(top=5, get_content=True, classify='全部')
