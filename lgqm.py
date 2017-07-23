# -*- coding: gbk -*-
import re,time
from urllib import request


def get_novel(url):
    with request.urlopen(url) as f:
        data=f.read().decode('gbk',errors='ignore')
        re_se=re.compile(r'&nbsp;&nbsp;&nbsp;&nbsp;(.*?)\<')
        grp=re_se.findall(data)
        title=re.search(r'\<h1\>(.*?)\<',data)
        grp.append(title.group(1))
        url_new=re.search(r'nextpage="(.*?)"',data)
        grp.append(url_new.group(1))
        return grp

def data_r(novel_data):
    with open('e:/lgqm.txt','a',encoding='utf-8') as lgqm:
        novel_data=get_novel(url)
        url_new=novel_data.pop()
        title=novel_data.pop()
        lgqm.write(title)
        time.sleep(5)
        lgqm.write('\n')
        for novel in novel_data:
            lgqm.write(novel)
        lgqm.write('\n')
    return url_new

#def url_getter(url_old):


if __name__=='__main__':
    url = 'http://www.xfqxsw.com/modules/article/reader.php?aid=1630&cid=999146'
    while url!="http://www.xfqxsw.com/book/lingaoqiming/":
        novel_data=get_novel(url)
        url=data_r(novel_data)
        print(url)
        #break
        #time.sleep(5)
    print('finish')
