import re
import time

import requests

urlprotocol = ""


# 获取并检验要爬取的网站
def url_get():
    """
        找出url中的域名
        比如从https://www.xiaogeng.top/article/page/id=3筛选出www.xiaogeng.top
    """
    # url = input("please input the url:")
    url = "http://scce.ustb.edu.cn/"
    try:
        kv = {'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/74.0.3729.131 Safari/537.36',
              'Connection': 'close'}
        requests.get(url, headers=kv)
        return url
    except Exception:
        print("your url is incorrect!!")
        return url_get()


def url_same(url):
    # 判断输入的网站使用的是https还是http
    urlprotocol = re.findall(r'.*(?=://)', url)[0]
    print('该站使用的协议是：' + urlprotocol)
    if len(re.findall(r'/', url)) > 2:
        if urlprotocol == 'https':
            sameurl = re.findall(r'(?<=https://).*?(?=/)', url)[0]
        else:
            sameurl = re.findall(r'(?<=http://).*?(?=/)', url)[0]
    else:
        url = url + '/'
        if urlprotocol == 'https':
            sameurl = re.findall(r'(?<=https://).*?(?=/)', url)[0]
        else:
            sameurl = re.findall(r'(?<=http://).*?(?=/)', url)[0]
    print('域名地址：' + sameurl)
    return urlprotocol + "://" + sameurl


# 爬取url页面中的链接
def get_page_include_url(url):
    kv = {'user_agent': 'Mozilla/5.0'}
    downloadimages = ""
    try:
        r = requests.get(url, headers=kv)
        r.encoding = r.apparent_encoding
        pagetext = r.text
        pagelinks = re.findall(r'(?<=href=").*?(?=")|(?<=href=\'). *?(?=\')', pagetext)
        downloadimages = re.findall(r'(?<=src=")(.+?\.jpg|png)(?=")|(?<=src=\').*?(?=\')', pagetext)
    except requests.exceptions.InvalidURL:
        pagelinks = ""
        print("Invalid URL " + url)
    except requests.exceptions.ConnectionError:
        pagelinks = ""
        print("Connection Error " + url)
    except Exception:
        pagelinks = ""
        print(str(Exception) + url)
    return pagelinks, downloadimages


# 将一个列表写入文件
def write2file(url_list):
    file = open('urls.txt', 'w')
    for url in url_list:
        file.write(url + '\n')
    file.close()


def write2images(url_list):
    file = open('images.txt', 'w')
    for url in url_list:
        file.write(url + '\n')
    file.close()
    i = 0
    for imageUrl in url_list:
        # with open(re.search(r".{4}.jpg|png", imageUrl).group(), 'wb') as f:
        i += 1
        try:
            with open(str(i) + re.search(r".jpg|png", imageUrl).group(), 'wb') as f:
                images = requests.get(imageUrl)
                time.sleep(0.1)
                f.write(images.content)
        except requests.exceptions.InvalidURL:
            print("Invalid URL " + imageUrl)
        except requests.exceptions.ConnectionError:
            print("Connection Error " + imageUrl)
        except Exception:
            print(str(Exception) + imageUrl)


# url集合，循环遍历会用到
class LinkQueue:
    def __init__(self):
        # 已访问的url集合
        self.visited = []
        # 待访问的url集合
        self.unvisited = []

    # 获取访问过的url队列
    def get_visited_url(self):
        return self.visited

    # 获取未访问的url队列
    def get_unvisited_url(self):
        return self.unvisited

    # 添加url到访问过得队列中
    def add_visited_url(self, url):
        return self.visited.append(url)

    # 移除访问过的url
    def remove_visited_url(self, url):
        return self.visited.remove(url)

    # 从未访问队列中取一个url
    def unvisited_url_dequeue(self):
        try:
            return self.unvisited.pop()
        except IndexError:
            return None

    # 添加url到未访问的队列中
    def add_unvisited_urllist(self, urllist):

        # 筛选pagelinks中的url
        def url_filtrate(pagelinks):
            """
            print("我现在在筛选")
            """
            i = 0
            # 补全网址
            while i < len(pagelinks):
                if re.match('@', pagelinks[i]) is True:
                    pagelinks[i] = ""
                elif re.match('tel:', pagelinks[i]) is True:
                    pagelinks[i] = ""
                elif re.match('.+\..+\..+', pagelinks[i]) is None:
                    pagelinks[i] = sameurl + pagelinks[i]
                i = i + 1
            # 去除不是该站点的url
            same_target_url = []
            for link in pagelinks:
                if re.findall(sameurl, link):
                    same_target_url.append(link)
            # 去除重复url
            unrepect_url = []
            for link in same_target_url:
                if link not in unrepect_url:
                    unrepect_url.append(link)
            return unrepect_url

        urllist = url_filtrate(urllist)
        for link in urllist:
            if link != "" and link not in self.visited and link not in self.unvisited:
                self.unvisited.append(link)
        return self.unvisited

        # 获得已访问的url数目

    def get_visited_url_count(self):
        return len(self.visited)

    # 获得未访问的url数目
    def get_unvisted_url_count(self):
        return len(self.unvisited)

    # 判断未访问的url队列是否为空
    def unvisited_url_empty(self):
        return len(self.unvisited) == 0


# 真正的爬取函数
class Spider:
    linkQueue: LinkQueue
    imageQueue: LinkQueue

    def __init__(self, url):
        self.linkQueue = LinkQueue()  # 引入linkQueue类
        self.imageQueue = LinkQueue()
        urllist = [url, ]
        self.linkQueue.add_unvisited_urllist(urllist)  # 并将需要爬取的url添加进linkQueue对列中

    def crawler(self):
        # i = 10
        while not self.linkQueue.unvisited_url_empty():  # 若未访问队列非空
            # time.sleep(0.01)
            # print("嘀嘀嘀我又爬到一个")
            # while i > 0:
            # i -= 1
            visited_url = self.linkQueue.unvisited_url_dequeue()  # 取一个url
            if visited_url is None or visited_url == '':
                continue
            print(visited_url)
            initial_links, images_links = get_page_include_url(visited_url)  # 爬出该url页面中所有的链接
            self.linkQueue.add_visited_url(visited_url)  # 将该url放到访问过的url队列中
            self.linkQueue.add_unvisited_urllist(initial_links)
            self.imageQueue.add_unvisited_urllist(images_links)

        print("哥我爬完了")
        return self.linkQueue.visited, self.imageQueue.unvisited


if __name__ == '__main__':
    url = url_get()
    sameurl = url_same(url)
    spider = Spider(url)
    urlList, imageList = spider.crawler()
    write2file(urlList)
    write2images(imageList)
