import requests
import json
import time
import random
import warnings
warnings.filterwarnings('ignore')

headers = {
        'Referer': 'https://web.thuhole.com/',
        'TE': 'trailers',
        'TOKEN': 'afge3swocqac7uzdko7wm4znnvowqhfm', # change your token here
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
}

headers_without_te = headers

proxies = {
        'http': 'socks5h://127.0.0.1:33211',
        'https': 'socks5h://127.0.0.1:33211'
}

def req_page(page:int):
    return requests.get(f"https://tapi.thuhole.com/v3/contents/post/attentions?page={page}&device=0&v=v3.0.6-455338", headers=headers, proxies=proxies,verify=False)


def get_attention_pages():
    """
    introduction
    ------------
    获取所有的关注树洞，按页数保存json文件

    Notes
    ----------
    一次性获取所有的关注列表，保存的文件名为attention_page_{i}.json
    """

    i = 1
    while True:
        with open(f'attention_page_{i}.json', 'wb') as f:
            res = req_page(i).content
            js = json.loads(str(res, encoding='utf-8'))
            f.write(res)
            print('page', i, 'done')
        if len(js['data']) == 0:
            break
        else:
            i += 1
            time.sleep(1)

def get_detail(pid):
    return requests.get(f'https://tapi.thuhole.com/v3/contents/post/detail?pid={pid}&device=0&v=v3.0.6-455338',
                        headers=headers, proxies=proxies,verify=False)

def get_all_details(prefix, begin, pages):
    """
    introduction
    ------------
    将所有**已经**爬取的json文件进行提取，按照树洞信息编号提取出单个文件

    params
    ------
    prefix:所要进行操作的json文件的前缀
    begin:开始页数
    pages:结束页数

    Notes
    ----------
    保存的文件名为{pid}.json
    若想对关注的树洞进行操作，则前缀为:attention_page_
    """
    for i in range(begin, pages + 1):
            print('Now begin page', i)
            with open(f'{prefix}{i}.json', 'r', encoding='utf-8') as f:
                res = json.load(f)
            for hole in res['data']:
                with open(f"{hole['pid']}.json", 'wb') as f:
                    try:
                        f.write(get_detail(hole['pid']).content)
                    except:
                        time.sleep(15)
                        f.write(get_detail(hole['pid']).content)
                    print('hole', hole['pid'], 'done')
                    time.sleep(1 + random.uniform(0, 0.8))



def req_key(page, key):
    return requests.get(f'https://tapi.thuhole.com/v3/contents/search?pagesize=50&page={page}&keywords={key}&device=0&v=v3.0.6-455338', headers=headers_without_te, proxies=proxies,verify=False)


def get_search_pages(key):
    """
    introduction
    ------------
    按照搜索值获取所有的树洞，按照页数保存json文件

    params
    ------
    key:搜索值

    Notes
    ----------
    保存的文件名为{key}.json
    """
    i = 1
    while True:
        time.sleep(1)
        with open(f'{key}{i}.json', 'wb') as f:
            res = req_key(i, key).content
            js = json.loads(str(res, encoding='utf-8'))
            f.write(res)
            print('page', i, 'done len', len(str(res, encoding='utf-8')))
            if len(js['data']) == 0:
                break
            else:
                i += 1
                time.sleep(1)


