# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import warnings
import re
from datetime import datetime
import json
import pandas as pd
import random
import time
import datetime
from multiprocessing import Pool


headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Referer':'https://www.bilibili.com/',
    'Connection':'keep-alive'}
    
cookies={'cookie':'LIVE_BUVID=AUTO6415404632769145; sid=7lzefkl6; stardustvideo=1; CURRENT_FNVAL=16; rpdid=kwmqmilswxdospwpxkkpw; fts=1540466261; im_notify_type_293928856=0; CURRENT_QUALITY=64; buvid3=D1539899-8626-4E86-8D7B-B4A84FC4A29540762infoc; _uuid=79056333-ED23-6F44-690F-1296084A1AAE80543infoc; gr_user_id=32dbb555-8c7f-4e11-beb9-e3fba8a10724; grwng_uid=03b8da29-386e-40d0-b6ea-25dbc283dae5; UM_distinctid=16b8be59fb13bc-094e320148f138-37617e02-13c680-16b8be59fb282c; DedeUserID=293928856; DedeUserID__ckMd5=6dc937ced82650a6; SESSDATA=b7d13f3a%2C1567607524%2C4811bc81; bili_jct=6b3e565d30678a47c908e7a03254318f; _uuid=01B131EB-D429-CA2D-8D86-6B5CD9EA123061556infoc; bsource=seo_baidu'}

def get_bilibili_oubing(url):
    avid=[]
    video_type=[]
    watch_count=[]
    comment_count=[]
    up_time=[]
    up_name=[]
    title=[]
    duration=[]
    
    print('正在爬取{}'.format(url))
    time.sleep(random.random()+2)
    res=requests.get(url,headers=headers,cookies=cookies,timeout=30)
    
    soup=BeautifulSoup(res.text,'html.parser')
    
    
    #avi号码
    avids=soup.select('.avid')
    
    #视频类型
    videotypes=soup.find_all('span',class_="type hide")

    #观看数
    watch_counts=soup.find_all('span',title="观看")
    
    #弹幕
    comment_counts=soup.find_all('span',title="弹幕")
    
    #上传时间
    up_times=soup.find_all('span',title="上传时间")
    
    #up主
    up_names=soup.find_all('span',title="up主")

    #title
    titles=soup.find_all('a',class_="title")
    #时长
    durations=soup.find_all('span',class_='so-imgTag_rb')
    
    for i in range(20):
        avid.append(avids[i].text)
        video_type.append(videotypes[i].text)
        watch_count.append(watch_counts[i].text.strip())
        comment_count.append(comment_counts[i].text.strip())
        up_time.append(up_times[i].text.strip())
        up_name.append(up_names[i].text)
        title.append(titles[i].text)
        duration.append(durations[i].text)
        
    result={'视频id':avid,'视频类型':video_type,'观看次数':watch_count,'弹幕数量':comment_count,'上传时间':up_time,'up主':up_name,'标题':title,'时长':duration}

    results=pd.DataFrame(result)
    return results

 
if __name__=='__main__': 
    url_original='http://search.bilibili.com/all?keyword=哪吒之魔童降世&from_source=nav_search&order=totalrank&duration=0&tids_1=0&page={}'
    url_click='http://search.bilibili.com/all?keyword=哪吒之魔童降世&from_source=nav_search&order=click&duration=0&tids_1=0&page={}'
    url_favorite='http://search.bilibili.com/all?keyword=哪吒之魔童降世&from_source=nav_search&order=stow&duration=0&tids_1=0&page={}'
    url_bullet='http://search.bilibili.com/all?keyword=哪吒之魔童降世&from_source=nav_search&order=dm&duration=0&tids_1=0&page={}'
    url_new='http://search.bilibili.com/all?keyword=哪吒之魔童降世&from_source=nav_search&order=pubdate&duration=0&tids_1=0&page={}'
    all_url=[url_bullet,url_click,url_favorite,url_new,url_original]

    info_df=pd.DataFrame(columns = ['视频id','视频类型','观看次数','弹幕数量','上传时间','up主','标题','时长']) 
    for i in range(50):
        for url in all_url:
            full_url=url.format(i+1)
            info_df=pd.concat([info_df,get_bilibili_oubing(full_url)],ignore_index=True)
      
    print('爬取完成！')
    #去重
    info_df=info_df.drop_duplicates(subset=['视频id'])
    info_df.info()
    info_df.to_excel('哪吒.xlsx')
        