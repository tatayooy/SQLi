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

# attract form from url
def get_form(url):
    opt = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=opt)
    res = driver.get(url)
    s = driver.page_source
    soup = BeautifulSoup(s, "lxml")
    soupl = BeautifulSoup(s, "html.parser")
    form = soup.find(class_='write')
    forml = soupl.find_all("form")
    if len(forml) <= 1 :
        return form
    else :
        return forml
        driver.close()


# get form details
def form_detail(form):
    formdt = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get")
    inputs = []

    for inputs_tag in form.find_all("input"):
        inputs_type = inputs_tag.attrs.get('type', 'text')
        inputs_name = inputs_tag.attrs.get('name')
        inputs_value = inputs_tag.attrs.get('value', '')
        inputs.append({"type":inputs_type, "name":inputs_name, "value":inputs_value})

    formdt['action'] = action
    formdt['method'] = method
    formdt['inputs'] = inputs
    return formdt

# check response for vanulable
def vuln(response):
      errors = {"syntax", "error", "success"}
      for error in errors:
          if error in response.content.decode().lower():
              print(f"--error response included the word [{error}]--")
              return True
      return False

# form scanner
def formscan(url, payload):
     forms = get_form(url)
     print(f"founded {len(forms)} forms on {url}")

     for form in forms:
        details = form_detail(form)

        for i in payload:
            data = {}
            for input_tag in details["inputs"]:
                if input_tag['type'] == "hidden" or input_tag["value"]:
                    data[input_tag['name']]=input_tag["value"]+i
                elif input_tag["type"]!="submit":
                    data[input_tag["name"]] = f"test{i}"

            form_detail(form)

            if details["method"] == "post":
                res = s.post(url, data=data)
            elif details["method"] == "get":
                res = s.get(url, params=data)
            if vuln(res):
                print(f"SQLi possible responded to {i}")
            else:
                print(f"SQLi not possible")
                break


if __name__ == "__main__":
    formscan(url, payload)



# formscan(url)
# form = get_form(url)
# form_detail(form)
# def separate_form(forms):
#     if len(forms) > 1:
#         i=1
#         while i <= len(forms):
#             singleform = forms[i-1]
#             print(F"{i}")
#             i = i+1
#     else:
#         return forms