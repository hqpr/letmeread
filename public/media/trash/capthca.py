import cookielib
import urllib2
import urllib
import re
import httplib, urllib

# getting picture
c = urllib.urlopen('http://www.livelib.ru/service/ratelimitcaptcha') # open 50 TV books
text = re.findall(r'[<]img.src\=\"(\/service\/captcha)', c.read())
captcha = ''
for t in text:
    pic = 'http://www.livelib.ru%s' % t
    result = urllib.urlretrieve(pic, 'captcha.jpg')
#print c.headers['Set-Cookie']

captcha = raw_input('Enter captcha: ')
values = {'form[captcha]': captcha}


params = urllib.urlencode({'form[captcha]': captcha})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
conn = httplib.HTTPConnection("www.livelib.ru/service/ratelimitcaptcha")
conn.request("POST", "", params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()

conn.close()



"""
for a, b in d:
    headers = {'LiveLibId': b}

    req = urllib2.Request(uri, captcha, headers=headers)  # without header
    response = urllib2.urlopen(req)
    the_page = response.read()
    if len(the_page) > 1128:
        print 'success! bitch!'
    else:
        print 'shit! shit! shit!'
        """