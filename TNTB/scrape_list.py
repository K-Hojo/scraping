import time
import re
from tenacity import retry, stop_after_attempt, wait_exponential
import requests
import lxml.html

TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504)

def scrape_list_page(res_list):
  html_list = lxml.html.fromstring(res_list.text)
  a_list = html_list.cssselect('#main table td.link > a') 
  a_list.reverse()
  for i in range(len(a_list)):
    url = return_url(a_list[i])
    yield url

def return_url(a):  
    url = a.get('href')  #本に書いてあるのはa.getだけどlistにはgetなんて属性ないぞって怒られた
    if url != None:
      #絶対パスでマッチ
      m = re.search(r'https*://1000ya.isis.ne.jp/([0-9]+).html',url)
      if m == None:
        #相対パスでマッチすれば絶対パスに変換
        m = re.search(r'/([0-9]+).html',url)
        if m != None:
          url = f'https://1000ya.isis.ne.jp{url}'
        #相対パスでもなければ個別対応
        else:  
          print(f'url={url}')
          while True:
            q = int(input('このリンクを登録しますか？はい：１、いいえ：０'))
            if q in {0,1}:
              break 
          if q:
            n = input('記事番号：')
            url = f'https://1000ya.isis.ne.jp/{n}.html'
    return url

def extract_no(url):
  m = re.search(r'https*://1000ya.isis.ne.jp/([0-9]+).html',url)
  return m.group(1)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
def fetch(url,session):
  # print(f'Retrieving{url}...')
  response = session.get(url)
  # print(f'Status: {response.status_code}')
  if response.status_code not in TEMPORARY_ERROR_CODES:
    return response
  raise Exception(f'Temporary Error: {response.status_code}')

s = requests.Session()
s.headers.update({'user-agent': 'hojo-crawler(k.hojo@gmail.com)'})
res_list = fetch('https://1000ya.isis.ne.jp/souran/index.php?vol=102',s)
for url in scrape_list_page(res_list):
  print(url)