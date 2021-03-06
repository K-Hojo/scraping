import time
import datetime
import re
from tenacity import retry, stop_after_attempt, wait_exponential
import requests

TEMPORARY_ERROR_CODES = (408, 500, 502, 503, 504)

def main():
  s = requests.Session()
  s.headers.update({'x-test': 'True'})
  # rr = requests.get('https://httpbin.org/status/500')
  # print(rr.text)
  # r = s.get('https://httpbin.org/status/500')
  # print(r.text)
  counter = 0
  while counter < 3:
    response = fetch('https://httpbin.org/status/500', s)
    print(datetime.datetime.now(), response.text)
    counter += 1
  
  
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1))
def fetch(url,session):
  # print(f'Retrieving{url}...')
  response = session.get(url)
  print(datetime.datetime.now(), f'Status: {response.status_code}')
  if response.status_code not in TEMPORARY_ERROR_CODES:
    return response
  raise Exception(f'Temporary Error: {response.status_code}')

main()