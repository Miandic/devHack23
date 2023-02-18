import requests

s = 'https://yandex.ru'
global SSL_flag
SSL_flag = True

def check_checker(s):
    try:
        requests.get(s)
    except Exception:
        return False



SSL_flag = check_checker(s)
if SSL_flag == None:
    SSL_flag = True

print("SSL:", SSL_flag)
