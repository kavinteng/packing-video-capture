import urllib.request
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

if __name__ == '__main__':
    while True:
        checknet = connect()
        if checknet is True:
            exit()
        else:
            pass