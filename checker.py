import requests

def SSL(url):
    try:
        requests.get(url)
    except requests.exceptions.SSLError:
        return False
    except Exception:
        return True
    return True


def normalize(url):
    if url[0:4] == 'http':
        return url
    else:
        return "https://"+url


def checkURL(link):
    link = normalize(link)
    ret = {
        "SSL": SSL(link),
        "Protocol": 'hz'
    }
    return ret

print(checkURL('info.cern.ch'))