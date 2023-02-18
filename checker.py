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
            return 2
        except KeyError:
            return 1
    except ssl.SSLCertVerificationError:
        return 0


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
    print(redirects)
    proto = redirects[rediCount]
    return proto, rediCount


def checkURL(link):
    ret = {
        "SSL": 1,
        "Protocol": False,
    }

    ret["SSL"] = CheckSSL(link)
    protocol, redirects = CheckRedirects(link)
    if protocol[0:5] == "https":
        ret["Protocol"] = True

    return ret

print(checkURL('info.cern.ch'))
print(checkURL('google.com'))
print(checkURL('thawte.com'))