import requests
from bs4 import BeautifulSoup
import time

# 登录微博，获取cookies
session = requests.Session()
login_url = 'https://passport.weibo.cn/signin/login'
data = {
    'username': 'your_username',
    'password': 'your_password',
    'savestate': '1',
    'r': '',
    'ec': '0',
    'pagerefer': '',
    'entry': 'mweibo',
    'wentry': '',
    'loginfrom': '',
    'client_id': '',
    'code': '',
    'qq': '',
    'mainpageflag': '1',
    'hff': '',
    'hfp': '',
}
session.post(login_url, data=data)
cookies = session.cookies.get_dict()

# 爬取微博话题的第一页内容
url = 'https://m.weibo.cn/api/container/getIndex?containerid=1008085a5b38f5b3edf7a3c3d3e3b8c1b10d1f_-_feed&luicode=10000011&lfid=100103type%3D1%26q%3D%23%E7%96%AB%E8%8B%97%E6%8E%A5%E7%A7%8D%23&featurecode=20000320&type=all&page=1'
headers = {
    'Referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%23%E7%96%AB%E8%8B%97%E6%8E%A5%E7%A7%8D%23',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
    'X-Requested-With': 'XMLHttpRequest',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cookie': '; '.join([f'{key}={value}' for key, value in cookies.items()]),
}
response = requests.get(url, headers=headers)
json_data = response.json()
cards = json_data['data']['cards']

# 遍历微博内容和评论
for card in cards:
    if card['card_type'] == 9:
        mblog = card['mblog']
        print('微博内容：', mblog['text'])
        if mblog.get('retweeted_status'):
            print('转发内容：', mblog['retweeted_status']['text'])
        if mblog.get('pics'):
            for pic in mblog['pics']:
                print('图片URL：', pic['large']['url'])
        if mblog.get('page_info'):
            print('链接标题：', mblog['page_info']['page_title'])
            print('链接URL：', mblog['page_info']['page_url'])
        comments_count = mblog['comments_count']
        if comments_count > 0:
            comments_url = f'https://m.weibo.cn/comments/hotflow?id={mblog["id"]}&mid={mblog["mid"]}&max_id_type=0'
            response = requests.get(comments_url, headers=headers)
            json_data = response.json()
            comments = json_data['data']['data']
            for comment in comments:
                print('评论：', comment['text'])
        print('---')
    time.sleep(1)
