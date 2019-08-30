"""
author: sky94520
desc: 按层级爬取github链接
    目前存在问题：
    1.get_items_from_url()可能会发生超时异常
    2.当下载失败时会写入到a.txt文件，缺少一个解析a.txt的功能
    3.多线程下载
    4.文件夹的path为空的问题
"""
import requests
from pyquery import PyQuery as pq
from urllib.parse import urljoin
import threading
from multiprocessing.pool import Pool
import os
import logging

import log


# 加锁，避免创建文件夹出错
lock = threading.Lock()


def get_items_from_url(url):
    """
    从url中获取html文本，解析后返回dict
    @param url 要解析的链接
    @return dict {'name' : '文件名', 'url' : '下载链接', "type": }
    """
    headers = {
        'Host': 'github.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    }
    response = requests.get(url=url, headers=headers)
    base_url = 'https://github.com'

    # 响应失败，则直接返回
    if response.status_code != 200:
        print('网页加载错误')
        return
    # 开始解析标签
    doc = pq(response.text)
    items = doc.find('tr.js-navigation-item').items()

    for item in items:
        a = item.find('.content span a')
        # 获取链接的文本
        name = a.text()
        if len(name) == 0:
            continue
        # 获取链接
        url = urljoin(base_url, a.attr('href'))
        # 是路径
        if url.find("blob") == -1:
            is_file = 0
        else:
            is_file = 1
            url = url.replace("blob", "raw")
        yield {
            'name': name,
            'url': url,
            'type': is_file
        }


def start_download(start_url, base_dir):
    """
    根据开始链接级联获取所有文件，根据base_dir确定根目录
    :param start_url:
    :param base_dir:
    :return:
    """
    # 解析完成的项列表
    groups = []
    # 等待跟进队列
    queue = [start_url]

    while len(queue) > 0:
        url = queue.pop()
        print("尝试爬取链接", url)
        # 尝试爬取链接
        for item in get_items_from_url(url):
            # 是路径，则放入队列中，等待跟进
            if item["type"] == 0:
                queue.append(item["url"])
            # 是文件，放入下载队列中
            elif item["type"] == 1:
                item["base_dir"] = base_dir
                groups.append(item)
    print('parse data success!!!')

    # 多线程下载
    pool = Pool()
    pool.map(download_file, groups)
    pool.close()
    pool.join()


def get_path_from_url(url, base_dir):
    """
    从url中根据base_dir获取之后的路径
    :param url:
    :param base_dir:
    :return:
    """
    # 根据根目录和链接来确定目录的层级
    index = url.find(base_dir)
    path = url[index:]
    path = os.path.split(path)[0]
    return path


def download_file(dic):
    """
    下载文件
    @:param dic {'name' : '文件名', 'url' : '链接'}
    """
    name, url, base_dir = dic["name"], dic["url"], dic["base_dir"]
    # 保证文件夹存在
    path = get_path_from_url(url, base_dir)
    if not os.path.exists(path):
        lock.acquire()
        try:
            print("尝试创建目录", path)
            os.makedirs(path)
        except FileExistsError:
            print("目录已经存在" % path)
        finally:
            lock.release()

    print('Ready download %s' % name)
    # 开始下载
    try:
        response = requests.get(url)
        file_path = os.path.join(path, name)

        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print('Successfully download %s' % name)
        else:
            print('%s already downloaded' % name)
    except requests.ConnectionError:
        logging.warning("Failed download:%s" % url)


if __name__ == '__main__':
    start_url = 'https://github.com/pbharrin/machinelearninginaction'
    base_dir = 'pbharrin'
    start_download(start_url, base_dir)
