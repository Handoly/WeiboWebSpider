import csv
from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import time
from tqdm import tqdm
import chardet

base_url = 'https://weibo.com/ajax/statuses/mymblog?'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36',
    'Referer': 'https://weibo.com/u/6856286875',
    'x-requested-with': 'XMLHttpRequest',
    'cookie': 'PC_TOKEN=cb5e738bb0; login_sid_t=8069876c2ee15b5e96fd228062a8b08c; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=807595280516.4688.1659273660724; SINAGLOBAL=807595280516.4688.1659273660724; ULV=1659273660727:1:1:1:807595280516.4688.1659273660724:; wb_view_log=1536*8641.25; XSRF-TOKEN=sbm31xnNBBuxJtes5_r0a95J; WBtopGlobal_register_version=2022073121; SSOLoginState=1659274013; SUB=_2A25P4vNMDeRhGeBJ71EY8SzPyDqIHXVtLJ0ErDV8PUJbkNAfLUXYkW1NRl248QX-LofbiOOdV9w3fa8N1agoewN2; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhMXhEZnKNBlJVUHSOJaiN55NHD95QcS0B01K2Ee0ecWs4Dqcj.i--4iKLsi-24i--Xi-zRiKLhi--fiKnNiKyhi--NiKysi-iW; WBPSESS=Dt2hbAUaXfkVprjyrAZT_PMgUSmk1HdL40W6G2dRw1Gf3PyDD_aottvFV7Ol4qFOFvQgoXKE6Kx3Dk-pz6NdZ9BQOAr9FVy8HkAvaiRrN0YGaBIEhKuT6da5J0KNPClo7Rg-hYHrtN3frBkcKwfOQcOi4ojOjs-n3aIclyaqO_Db_1wYLzlR17EKLYwegzDvoqLhi0RJAHWxtz_Q_fnAKA=='
}


def get_page(page):
    params = {
        'uid': '6856286875',
        'page': page,
        'feature': '0'
    }

    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('错误', e.args)


def parse_page(json):
    if json:
        items = json.get('data').get('list')
        for i in range(len(items)):
            weibo = {}
            weibo['发布时间'] = items[i].get('created_at')
            weibo['点赞数'] = items[i].get('attitudes_count')
            weibo['评论数'] = items[i].get('comments_count')
            weibo['转发数'] = items[i].get('reposts_count')
            weibo['内容'] = pq(items[i].get('text')).text()
            yield weibo




if __name__ == '__main__':
    pbar = tqdm(total=117, desc="Count", unit="times")
    with open('weibo_data.csv','a',encoding='gbk',newline='') as csvfile:
        fieldnames = ['发布时间','点赞数','评论数','转发数','内容']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for page in range(1,6):
            json = get_page(page)
            results = parse_page(json)
            time.sleep(1)  # 延时1秒
            for result in results:
                try:
                    writer.writerow(result)
                except Exception as e:
                    writer.writerow({'发布时间':'Null','点赞数':'Null','评论数':'Null','转发数':'Null','内容':'Null'})
                    pbar.update(1)  # 进度条更新
                else:
                    pbar.update(1)  # 进度条更新


