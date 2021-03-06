import re
import requests
import lxml.html

def scrape_detail_page(res_det, url):
  html_det = lxml.html.fromstring(res_det.text)
  # book_info = {
  #   'url' : url,
  #   'author' : html_det.cssselect('#default_style_area > div:nth-child(1) > div > div:nth-child(2)')[0].text,
  #   'title' : html_det.cssselect('#default_style_area > div:nth-child(1) > div > div:nth-child(6)')[0].text_content(),
  # }
  a = html_det.cssselect('#honbun p a')
  for i in range(len(a)):
    url = a[i].get('href')
    if url ==None:
      continue
    else:
      print(url)
  # links = []
  # for i in range(len(refs)): 
  #   ref_no = extract_no(refs[i].get('href'))
  #   if ref_no not in links:
  #     links.append(ref_no)
  # print([book_info, links])

def extract_no(url):
  return re.search(r'https*://1000ya.isis.ne.jp/([0-9]+).html',url).group(1)

url = 'https://1000ya.isis.ne.jp/0002.html'
res_det = requests.get(url,headers={'user-agent': 'hojo-crawler(k.hojo@gmail.com)'})
scrape_detail_page(res_det,url)