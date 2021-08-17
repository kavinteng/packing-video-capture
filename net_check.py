import urllib.request

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
    
print('Connected' if connect() else 'No Internet connection!')