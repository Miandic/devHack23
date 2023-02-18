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
    try:
        r = requests.get(link)
    except requests.exceptions.MissingSchema:






def checkURL(link):
    ret = {
        "SSL": 1,
        "Protocol": True,
        "Reachable": True
    }

    ret["SSL"] = CheckSSL(link)
    CheckRedirects(link)
    return ret

print(checkURL('info.cern.ch'))
print(checkURL('google.com'))
print(checkURL('thawte.com'))