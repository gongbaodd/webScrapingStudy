import requests
r = requests.get('http://www.baidu.com')
if r.status_code == 200:
    print(r.text[:250])
else:
    print(r.status_code)
