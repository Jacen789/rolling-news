# -*- coding: utf-8 -*-

import os
import re
import shutil
import zlib
import pickle
from urllib.parse import urlsplit
from datetime import datetime, timedelta


class DiskCache:
    """磁盘缓存"""

    def __init__(self, cache_dir='cache', expires=timedelta(days=30), compress=True):
        """
        cache_dir: 缓存的根级别文件夹
        expires: 缓存项被视为过期之前的时间增量
        compress: 是否压缩缓存中的数据
        """
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress

    def __getitem__(self, url):
        """从磁盘加载此 url 的数据
        """
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                result, timestamp = pickle.loads(data)
                if self.has_expired(timestamp):
                    raise KeyError(url + ' has expired')
                return result
        else:
            # url 的数据尚未缓存
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """将数据保存到此 url 的磁盘
        """
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        data = pickle.dumps((result, datetime.utcnow()))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as fp:
            fp.write(data)

    def __delitem__(self, url):
        """删除此 url 的数据和所有空的子目录
        """
        path = self.url_to_path(url)
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass

    def url_to_path(self, url):
        """为此 url 创建文件系统路径
        """
        components = urlsplit(url)
        # 当路径为空，设置为 /index.html
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        # 替换无效字符
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        # 限制最大字符数
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)

    def has_expired(self, timestamp):
        """返回此时间戳是否已过期
        """
        return datetime.utcnow() > timestamp + self.expires

    def clear(self):
        """删除所有缓存的数据
        """
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
