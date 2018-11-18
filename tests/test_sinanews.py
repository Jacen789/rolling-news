# -*- coding: utf-8 -*-

from rlnews import sinanews


def test_sinanews():
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='全部', path='全部.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='国内', path='国内.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='国际', path='国际.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='社会', path='社会.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='体育', path='体育.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='娱乐', path='娱乐.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='军事', path='军事.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='科技', path='科技.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='财经', path='财经.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='股市', path='股市.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='美股', path='美股.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='国内_国际', path='国内_国际.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='国内_社会', path='国内_社会.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='国际_社会', path='国际_社会.csv')
    sinanews.get_rolling_news_csv(top=5, get_content=True, classify='国内国际社会', path='国内国际社会.csv')
