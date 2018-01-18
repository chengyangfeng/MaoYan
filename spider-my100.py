#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/8 9:31
# @Author  : Aries
# @Site    : 
# @File    : spider-my100.py
# @Software: PyCharm Community Edition
#爬取猫眼电影top100
import json
import requests
from requests.exceptions import RequestException
import re
def getpage(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None
def parsepage(html):
    # pass
    pattern=re.compile('<dd.*?<i.*?>(.*?)</i>.*?title="(.*?)".*?data-src="(.*?)".*?class="star">(.*?)</p>.*?class="releasetime">(.*?)</p>.*?',re.S)
    results=re.findall(pattern,html)
    for result in results:
        yield {
            'index':result[0].strip(),
            'name': result[1].strip(),
            'image': result[2].strip(),
            'actor': result[3].strip(),
            'releasetime': result[4].strip()
        }
def writefile(content):
    with open('E:/awesome-python3-webapp/猫眼电影top100.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()
def save_image(img_url,img_name):
    response=requests.get(img_url)
    result=response.content
    filename=img_name
    fpath = 'E:/awesome-python3-webapp/download/' + filename+'.jpg'
    with open(fpath,'wb') as f:
        f.write(result)
        f.close()

def main():
    offset=0
    while offset<101:
        url='http://maoyan.com/board/4?offset='+str(offset)
        html=getpage(url)
        offset+=10
        for item in parsepage(html):
            writefile(item)
            img_url=item["image"]
            img_name=item["name"]
            save_image(img_url,img_name)
    print('排名保存成功')
    print('图片保存成功')
if __name__=='__main__':
    main()