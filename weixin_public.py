__author__ = 'marc'
#coding:UTF-8
import requests
import re
import pymysql
from bs4 import BeautifulSoup
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

js_list={u'知影':u'http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt6Ltxtwbmm6eQaBtwArtHi8&eqs=ZVsXolcgGwFLoGrnF%2BxpUuF9F9O305uJGXCQ3nIot8f95%2BD2G0%2Fd6w4QjhQUJr1fUAsAT&ekv=7&page=1',
           u'良仓':u'http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt9aE-GHf7Ne-t4i4bOhE3Go&eqs=Qmsoo7wgR%2FElop0BVF8WYumX2F9NE7wXMTJ7Cc1UWOmvCBFYt%2BdZk83wXIMXwv0P6hQ80&ekv=7&page=1' ,
         u'健身先健脑':u'http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt6kiQvot0lv-G4yXtsV6aGQ&eqs=HUsGoKMgoq90o2DAQMmoEuYAf5f2Cb%2FP75qfnxWiVc%2FAHo5K8I4HE3sqZkVoRxc8W8Jgb&ekv=7&page=1',
         u'财新Enjoy雅趣':u'http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFtyM57IXJydxDq7e2dfI5DWo&eqs=UxsioUig1h%2FroW9pD1%2FeuuzNCnCc%2FBwW%2FW%2B9zOC3asJ%2FEsp5JXZBQZj%2FOXiBO5TFZyrUs&ekv=7&page=1',
         u'Python开发者':u'http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFt5QBSP8mn4Jx2WSGw_rCNzQ&eqs=qhs9oUAgGopVo4ijtfSaguT9nMY9WgKrTYOtMi6qXbD4llISIT%2BG6aKYFIXisCp52igTG&ekv=7&page=1',
        u'数据挖掘DW':u'http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFtwUwT3YLdH8NLEW7Txt3rFk&eqs=HSs2ojAgtDtkovIt85c6ruHQIaNpu2R8einYws0x1Rn7CZHvIsVC4aOE6aosbN3mgwQHu&ekv=7&page=1',
         }

openid_list={u'知影':u'oIWsFt6Ltxtwbmm6eQaBtwArtHi8',
                u'良仓':u'oIWsFt9aE-GHf7Ne-t4i4bOhE3Go',
             u'健身先健脑':u'oIWsFt6kiQvot0lv-G4yXtsV6aGQ',
             u'财新Enjoy雅趣':u'oIWsFtyM57IXJydxDq7e2dfI5DWo',
             u'Python开发者':u'oIWsFt5QBSP8mn4Jx2WSGw_rCNzQ',
            u'数据挖掘DW':u'oIWsFtwUwT3YLdH8NLEW7Txt3rFk',
             }

template_1 = re.compile(r'\[CDATA\[http://mp.*?\]')
template_2 = re.compile(r'http://mp.*[^]]')
dic = {}

def check_article_exist(open_id, want_article):
    try:
        wp = pymysql.connect(host='localhost',user='test',passwd='test',db='newdb',charset='utf8')
        con = wp.cursor()
        num = con.execute('select * from weibo_public where open_id=%s and article_name=%s',(open_id,want_article))
        wp.close()
        if num>0:
            return True
        else:
            return False
    except:
        wp.close()
        print "ckeck failed : cannt connect to mysql"

def insert_record(open_id, want_article):
    try:
        wp = pymysql.connect(host='localhost',user='test',passwd='test',db='newdb',charset='utf8')
        con = wp.cursor()
        con.execute('insert into weibo_public(open_id, article_name) values (%s,%s)',(open_id,want_article))
        wp.commit()
        wp.close()
    except:
        wp.close()
        print "insert failed :cannt connect to mysql"

def get_article_name(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text)
    title = soup.h2.contents[0].title()
    return title

def write_link_to_html(link,name):
    wholename = 'email_store/'+ name +'.html'
    res = requests.get(link)
    bsoup = BeautifulSoup(res.content)

    imgs = bsoup('img')

    for img in imgs:
        if 'data-src' in img.attrs.keys():
            src_link = img['data-src']
            for pro in img.attrs.keys():
                del img[pro]
            img['src'] = src_link

    with open(wholename,'w') as f:
        f.write(str(bsoup))
    f.close()

    print 'write '+wholename+' already.'


def send_email(name):
    wholename = 'email_store/'+ name +'.html'
    fromaddr = "353350024@qq.com"
    toaddr = "353350024@qq.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = name
    with open(wholename,'r') as f:
        body = f.read()
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.qq.com','25')
    server.login("353350024@qq.com","msy19920105qq")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    print "send"+name+"successfully"

def main():
    for name in js_list.keys():
        dic.setdefault(name,[])
        url = js_list[name]
        r = requests.get(url)
        content = r.text
        match_list = template_1.findall(content)
        for i in range(len(match_list)):
            match_list[i] = template_2.findall(match_list[i])[0]
        dic[name]=match_list

    for name in dic.keys():
        open_id = openid_list[name]
        link_list = dic[name]
        for want_link in link_list[0:5]:
            want_article = get_article_name(want_link)
            if not check_article_exist(open_id,want_article):
                insert_record(open_id,want_article)
                write_link_to_html(want_link,want_article)
                send_email(want_article)
    print "mission is done!"











# with open("test.html", 'w+') as w:
#     w.write(html_public.read())
#
# soup = BeautifulSoup(html_public)
#
# res = soup.find('div', {'class', 'results'})
# lst = soup.findAll('div', {'id', 'sogou_vr_11002601_box_0'})
# if lst:
#     for content in lst:
#         print content