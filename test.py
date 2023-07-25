import sys
import requests
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# get argument
ps = argparse.ArgumentParser()
ps.add_argument("-u", "--url",dest='url', help='specify the target site')
#ps.add_argument("-p", "--payload",dest='pn', help='specify the payload')
option = ps.parse_args()
url = option.url
#PN = optio

# set payload
#payload = ["test' ", "test' --", " ' ", "\"", "test@gmail.com '", "test@gmail.com ' --", " ' or 1 = 1 ' ", " ' or 1 = 1 ' --"]
payload = []
# set header user-agent
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'
opt = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=opt)
res = driver.get(url)
s = driver.page_source
soup = BeautifulSoup(s, 'lxml')
form = soup.find('ul', class_='write')
print(type(form))
    # if lens(form) < 1:
    #     souph = BeautifulSoup(s, "html.parser")
    #     formh = souph.find_all("form")
    #     return formh
    #else :
driver.close()