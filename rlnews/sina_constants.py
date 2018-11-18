# -*- coding: utf-8 -*-

template_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num={}&page={}&r={}'

lid2classification = {
    "2509": "全部",
    "2510": "国内",
    "2511": "国际",
    "2669": "社会",
    "2512": "体育",
    "2513": "娱乐",
    "2514": "军事",
    "2515": "科技",
    "2516": "财经",
    "2517": "股市",
    "2518": "美股",
    "2968": "国内_国际",
    "2970": "国内_社会",
    "2972": "国际_社会",
    "2974": "国内国际社会"
}
classification2lid = dict((v, k) for k, v in lid2classification.items())
classifications = list(lid2classification.values())  # 新闻类别
max_num_per_page = 50

columns = ['classify', 'title', 'time', 'url', 'wapurl', 'media_name', 'keywords', 'content']
