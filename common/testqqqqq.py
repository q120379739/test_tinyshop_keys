import requests

url = "http://localhost:8080/TinyShopV3/index.php?con=simple&act=login_act"

# querystring = {"con":"index","act":"index"}

payload = {"redirectURL":"","account":"120379739@qq.com","password":"123456","tiny_token_login":""}
headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    'connection': "keep-alive",
    'content-length': "158",
    'content-type': "application/x-www-form-urlencoded",
    'cookie': "PHPSESSID=3e33a976e8d64a100cfcdd1395e53229,PHPSESSID=3e33a976e8d64a100cfcdd1395e53229; PHPSESSID=263e82123d3a333f9739c7b5e35da9da",
    'host': "192.168.3.207",
    'origin': "http://192.168.3.207",
    'referer': "http://192.168.3.207/TinyShopV3/index.php?con=simple&act=login",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
    'Cache-Control': "no-cache",
    'Postman-Token': "29ebaef1-2876-4fa7-9067-6398ad53d090,55bb266f-2849-49bb-9267-db0ace725cfa",
    'cache-control': "no-cache"
    }

response = requests.request("POST", url, data=payload)

print(response.text)