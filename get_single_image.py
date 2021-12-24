# coding=utf-8
# @Time : 2021/12/24 1:55
# @Author : Karasukaigan
# @File : get_single_image.py
# @Software : PyCharm

import requests
import re
import os
import time
import random
import json


def main():
    folder_name = 'single_img'  # 指定目录
    url = ''  # 帖子地址，格式为https://www.instagram.com/p/……/
    cookie = ''  # 自己的cookie，使用抓包工具获得

    download_helper(folder_name, url, cookie)


def download_helper(folder_name, url, cookie):
    url_list, name_list = get_img_url(url, cookie)  # 获取图片地址
    download_img(url_list, name_list, folder_name)  # 下载图片


def get_img_url(url, cookie):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'dnt': '1',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.131 Safari/537.36 '
    }
    
    # 获取HTML
    print("请求 -> " + url)
    response = requests.get(url, headers=headers)
    html_data = response.text

    url_list = []
    name_list = []

    # 提取HTML中的图片URL，适用于多张图片或部分单张图片的帖子
    url_list1 = re.findall('https://scontent-lax3-1.cdninstagram.com(.+?)",', html_data)
    for i in range(len(url_list1)):
        url_list1[i] = "https://scontent-lax3-1.cdninstagram.com" + url_list1[i]
    url_list2 = re.findall('https://scontent-lax3-2.cdninstagram.com(.+?)",', html_data)
    for i in range(len(url_list2)):
        url_list2[i] = "https://scontent-lax3-2.cdninstagram.com" + url_list2[i]
    url_list3 = url_list1 + url_list2
    for i in range(len(url_list3)):
        if url_list3[i].find("1080x1080") != -1:
            url_list.append(url_list3[i].replace("\\u0026", "&"))
    for i in range(len(url_list)):
        print(url_list[i])

    # 如用上面的方法提取不成功
    if not url_list:
        # 查找JSON，获取图片URL
        page_data = re.findall('<script type="text/javascript">window.__additionalDataLoaded(.+?)\);</script>', html_data)
        img_data = json.loads(page_data[0].split(",", 1)[1]);
        url_list.append(img_data['graphql']['shortcode_media']['display_url'])
        for i in range(len(url_list)):
            print(url_list[i])

    # 提取图片名
        for i in range(len(url_list)):
            name_list.append(url_list[i].split("/")[6].split("?")[0])
    else:
        for i in range(len(url_list)):
            name_list.append(url_list[i].split("/")[7].split("?")[0])

    return url_list, name_list


# 下载图片到本地
def download_img(url_list, name_list, folder_name):
    num = len(url_list)
    for i in range(num):
        # 如果该图片未被下载过则下载，这避免了重复下载相同的图片
        if not os.path.exists(folder_name + '/' + name_list[i]):
            # 请求图片
            img = requests.get(url_list[i])
            time.sleep(random.randint(10, 20) * 0.1)
            # 如果没有对应文件夹则创建文件夹
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            # 保存到文件
            f = open(folder_name + '/' + name_list[i], 'wb')
            f.write(img.content)
            f.close()
        print("下载进度(" + str(i + 1) + "/" + str(num) + ")")
    print("下载完成，已保存到" + os.getcwd() + "\\" + folder_name)


if __name__ == "__main__":
    main()