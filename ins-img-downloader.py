# coding=utf-8
# @Time : 2021/12/23 22:25
# @Author : Karasukaigan
# @File : ins-img-downloader.py
# @Software : PyCharm

import requests
import os
import random
import json
import time


def main():
    user_name = ''  # Ins用户名
    url = ''  # 以“?query_hash=”为开头的请求的地址，使用抓包工具获得
    cookie = ''  # 自己的cookie，使用抓包工具获得

    download_helper(user_name, url, cookie)


def download_helper(user_name, url, cookie):
    referer = "https://www.instagram.com/" + user_name + "/"  # Ins个人主页地址
    url_list = []
    id_list = []
    downloaded_num = 0

    # 利用get_img_url_to_end()获取所有图片的真实地址，发生错误可自动从断点处继续
    var = 1
    while var == 1:
        # 获取图片真实地址
        url_list_new, id_list_new, breakpoint_url, downloaded_num = get_img_url_to_end(url, cookie, referer, downloaded_num)
        url_list += url_list_new
        id_list += id_list_new
        url = breakpoint_url

        # 如果顺利获得所有URL，则跳出循环
        if breakpoint_url == 'none':
            break
        # 如果因错误中断，则暂停程序一定时间后再继续执行
        else:
            stop_time = 60
            print("暂停" + str(stop_time) + "秒")
            time.sleep(stop_time)

    # 下载图片到本地
    download_img(url_list, id_list, user_name)


# 获取图片地址，返回图片的URL和ID列表
def get_img_url_to_end(url, cookie, referer, downloaded_num):
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
        'cookie': cookie,
        'dnt': '1',
        'referer': referer,
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.131 Safari/537.36 '
    }

    url_list = []
    id_list = []
    num = downloaded_num

    # 循环，直到解析完所有图片的真实地址
    var = 1
    while var == 1:
        try:
            print("请求 -> " + url)
            response = requests.get(url, headers=headers)
            time.sleep(random.randint(10, 20) * 0.1)
            data = response.json()  # 将响应的数据转成JSON
            if num == 0:
                print('总数：' + str(data['data']['user']['edge_owner_to_timeline_media']['count']))

            # 提取URL和ID，并将其添加到列表url_list和id_list中
            for i in range(12):
                try:
                    for j in range(len(data['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node'][
                                           'edge_sidecar_to_children']['edges'])):
                        url_list.append(data['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node'][
                                            'edge_sidecar_to_children']['edges'][j]['node']['display_url'])
                        id_list.append(data['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node'][
                                           'edge_sidecar_to_children']['edges'][j]['node']['id'])
                except KeyError:
                    url_list.append(
                        data['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['display_url'])
                    id_list.append(data['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['id'])
                    num += 1
                else:
                    num += 1
            print('解析进度(' + str(num) + '/' + str(data['data']['user']['edge_owner_to_timeline_media']['count']) + ')')

            # 如果获取完全部URL则跳出循环
            if num >= data['data']['user']['edge_owner_to_timeline_media']['count'] or \
                    not (data['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']):
                break

        except json.decoder.JSONDecodeError:
            print("json.decoder.JSONDecodeError")
            breakpoint_url = url
            downloaded_num = num - 12
            print("断点：" + breakpoint_url)
            print("URL列表：" + str(url_list))
            print("ID列表：" + str(id_list))
            return url_list, id_list, breakpoint_url, downloaded_num
        except KeyError:
            print("KeyError")
            breakpoint_url = url
            downloaded_num = num - 12
            print(data)
            print("断点：" + breakpoint_url)
            print("URL列表：" + str(url_list))
            print("ID列表：" + str(id_list))
            return url_list, id_list, breakpoint_url, downloaded_num
        except IndexError:
            print("IndexError")
            breakpoint_url = url
            downloaded_num = num - 12
            print("断点：" + breakpoint_url)
            print("URL列表：" + str(url_list))
            print("ID列表：" + str(id_list))
            breakpoint_url = 'none'
            return url_list, id_list, breakpoint_url, downloaded_num
        else:
            pass

        # 更新请求地址
        next_pointer = data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor'].split("=")
        url_breakdown = url.split("first%22%3A12%")
        url = url_breakdown[0] + "first%22%3A12%2C%22after%22%3A%22" + next_pointer[0] + "%3D%3D%22%7D"

    breakpoint_url = "none"
    downloaded_num = num
    print("URL列表：" + str(url_list))
    print("ID列表：" + str(id_list))
    return url_list, id_list, breakpoint_url, downloaded_num


# 下载图片到本地
def download_img(url_list, id_list, user_name):
    num = len(url_list)
    folder = user_name
    for i in range(len(url_list)):
        # 如果该图片未被下载过则下载，这避免了重复下载相同的图片
        if not os.path.exists(folder + '/' + id_list[i] + '.jpg'):
            # 请求图片
            img = requests.get(url_list[i])
            time.sleep(random.randint(10, 20) * 0.1)
            # 如果没有对应文件夹则创建文件夹
            if not os.path.exists(folder):
                os.makedirs(folder)
            # 保存到文件
            f = open(folder + '/' + id_list[i] + '.jpg', 'wb')
            f.write(img.content)
            f.close()
        print("下载进度(" + str(i + 1) + "/" + str(num) + ")")
    print("下载完成，已保存到" + os.getcwd() + "\\" + folder)


if __name__ == "__main__":
    main()
