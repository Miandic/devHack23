import ssl, socket, requests

def CheckSSL(link):
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(socket.socket(), server_hostname=link)
    try:
        s.connect((link, 443))
        cert = s.getpeercert()

        subject = dict(x[0] for x in cert['subject'])
        try:
            subject["businessCategory"]
            return "STRONG"
        except KeyError:
            return "OK"
    except ssl.SSLCertVerificationError:
        return "NO"
    except Exception:
        return "error occuried with this url"


def CheckRedirects(link):
    redirects = []
    try:
        r = requests.get(link)
        for i in r.history:
            redirects.append(i.url)
        redirects.append(r.url)
    except requests.exceptions.MissingSchema:
        try:
            r = requests.get("https://" + link)
            for i in r.history:
                redirects.append(i.url)
            redirects.append(r.url) 
        except requests.exceptions.SSLError:
            r = requests.get("http://" + link)
            for i in r.history:
                redirects.append(i.url)
            redirects.append(r.url)
            
    rediCount = len(redirects) - 1
    finalUrl = redirects[rediCount]
    #print(redirects)
    proto = redirects[rediCount]
    return proto, rediCount, finalUrl


def CheckURL(link):
    print(link)
    ret = {
        "SSL": "OK",
        "Protocol": "http",
        "Redirects": "0",
        "Result": "idk"
    }
    cnt = 0
    ret["SSL"] = CheckSSL(link)
    if ret["SSL"] == "STRONG":
        cnt = 5
    if ret["SSL"] == "OK":
        cnt += 1
    
    protocol, redirects, finalUrl = CheckRedirects(link)
    if protocol[0:5] == "https":
        ret["Protocol"] = "https"
        cnt += 1
    ret["Redirects"] = str(redirects)
    
    while redirects > 0:
        redirects -= 1
        cnt -= 0.3

    if cnt >= 2:
        ret["Result"] = "Great"
    elif cnt < 1:
        ret["Result"] = "Sus"
    else:
        ret["Result"] = "Ok"

    ret["URL"] = finalUrl
    
    return ret


print(CheckSSL('https://www.hellotech.com/'))