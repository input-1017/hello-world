# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import time

url = "https://www.everyonepiano.cn/Music-class12-%EF%BF%BD%EF%BF%BD%EF%BF%BD%EF%BF%BD.html?&p="

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/87.0.4280.141 Safari/537.36"}

rate_of_progress = 0


def request_(count):  # 主网页
    print('开始')
    Url_name_re = re.compile('<a class="Title" href="(.*?)" target="_blank" title="(.*?)"')  # 分别是网址和名字(没用上)
    first_url_list = []

    response = requests.get(url=url + str(count), headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")

    first_page = soup.find_all('div', class_='MITitle')  # 每个歌曲清单都放这里

    for i in first_page:
        first_url = re.findall(Url_name_re, str(i))
        first_url_list.append(first_url)

    print('(1)第一请求完毕...')
    return first_url_list


def url_name(count):  # 把每个first_url_list都变成可以请求的
    first_url_list = request_(count)

    url_head = 'https://www.everyonepiano.cn/'
    url_list = []

    for i in first_url_list[1:]:  # 第一个不是
        for T_url in i:
            url_list.append(url_head + str(T_url[0]))

    print('(2)完整url请求完毕')
    return url_list


def deep_url(count):  # 获取每张曲谱的url
    url_list = url_name(count)

    first_re = re.compile('<a href="(.*?)" onclick="pianocount')
    MusicScore_count_re = re.compile('\d')  # 每个曲子有好几个谱子
    deep_url_list = []

    print('图片网址获取中...')
    for i in url_list:
        response = requests.get(url=i, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        a = soup.find_all('small')  # 曲谱数都放在这个标签下
        page_count = re.findall(MusicScore_count_re, str(a[1]))

        first = soup.find_all('div', class_='EOPSingleWuxianpu')  # 每个deep_url和名字都放在这个标签下

        re_find = re.findall(first_re, str(first))
        for c in page_count:  # c是个list
            deep_url_list.append(re_find[-(int(c)):])  # 只有最后c个是有用的

    print('(3)获取完毕')
    return deep_url_list


def deep_url_name(count):  # 使deep_url_list可以被请求
    deep_url_list = deep_url(count)

    pic_url = []

    print('请求图片中...')
    for i in deep_url_list:
        for a in i[:-1]:
            pic_url.append('https://www.everyonepiano.cn/' + str(a))

    print('(4)请求完毕')
    return pic_url


def picture_url(count):  # 获取每个曲谱图片的独立网址
    pic_list = deep_url_name(count)

    MusicScore_pic_re = re.compile('<img alt="(.*?)" class="img-responsive DownMusicPNG" src="(.*?)"')
    end_url_list = []
    end_name_list = []

    print('获取图片中...')
    for i in pic_list:
        response = requests.get(url=i, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        first = soup.find_all('div', class_='EOPStavePIC')  # 图片网址和名字在这个标签下

        end_MusicScore_pic_url_list = re.findall(MusicScore_pic_re, str(first))

        for a in end_MusicScore_pic_url_list:
            end_name = "https://www.everyonepiano.cn" + str(a[1])  # 加上开头
            end_url_list.append(end_name)
            end_name_list.append(a[0])

    print('(5)获取完毕')
    return end_url_list, end_name_list


def Keep_picture(count):  # 保存图片
    end_url_name_list = picture_url(count)

    for i, a in zip(end_url_name_list[0], end_url_name_list[1]):  # i为网址, a为名字
        response = requests.get(url=i, headers=headers)

        context = response.content

        f = open('/Users/lbq/Downloads/mac_file/music/{0}.png'.format(str(a)), 'wb')
        f.write(context)

        f.close()
        print('{0}  以下载完毕'.format(str(a)))

    print('第{0}页下载完毕'.format(count))


if __name__ == '__main__':
    print('-' * 50 + '曲谱爬取' + '-' * 50)
    count = input('从第几页开始(默认从第一页):')
    if count == '':
        count = 1
    end = input('爬取几页(默认为一页):')
    if end == '':
        end = 1
    time_ = input('每页停顿的时间(默认为3秒):')
    if time_ == '':
        time_ = 3

    count = int(count)
    p = 1

    while int(end) >= p:
        s = time.time()
        Keep_picture(int(count))
        e = time.time()

        time.sleep(int(time_))
        print('第%s页 耗时:' % str(count) + str(e - s - int(time_)))
        count += 1
        p += 1
