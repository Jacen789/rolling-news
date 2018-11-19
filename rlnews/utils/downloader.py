# -*- coding: utf-8 -*-

import time
import random
import socket
import urllib.parse
import urllib.request
from datetime import datetime

DEFAULT_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
DEFAULT_DELAY = 5
DEFAULT_RETRIES = 1
DEFAULT_TIMEOUT = 60


class Downloader:
    def __init__(self, delay=DEFAULT_DELAY, user_agent=DEFAULT_AGENT, proxies=None, num_retries=DEFAULT_RETRIES,
                 timeout=DEFAULT_TIMEOUT, opener=None, cache=None):
        socket.setdefaulttimeout(timeout)
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_retries = num_retries
        self.opener = opener
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result = self.cache[url]
            except KeyError:
                # url 在缓存中不可用
                pass
            else:
                if (not result['code']) or (self.num_retries > 0 and 500 <= result['code'] < 600):
                    # 服务器错误, 因此忽略 result 中的缓存，重新下载
                    result = None
        if result is None:
            # result 没有从缓存加载, 所以仍然需要下载
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {'User-agent': self.user_agent}
            result = self.download(url, headers, proxy=proxy, num_retries=self.num_retries)
            if self.cache:
                # 将 result 保存到缓存
                self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_retries, data=None):
        print('Downloading:', url)
        request = urllib.request.Request(url, data, headers or {})
        opener = self.opener or urllib.request.build_opener()
        if proxy:
            proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except Exception as e:
            print('Download error:', str(e))
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if num_retries > 0 and 500 <= code < 600:
                    # 5XX HTTP 错误，重新下载
                    return self.download(url, headers, proxy, num_retries - 1, data)
            else:
                code = None
        return {'html': html, 'code': code}


class Throttle:
    """通过在请求同一域之间休眠一段时间来限制下载
    """

    def __init__(self, delay):
        # 每个域的下载之间的延迟量
        self.delay = delay
        # 上次访问域的时间戳
        self.domains = {}

    def wait(self, url):
        """如果最近访问过此域则进行延迟
        """
        domain = urllib.parse.urlsplit(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()
