from bottle import route, run, request
from bs4 import BeautifulSoup
import urllib
import sys
import os
from threading import Timer

url = 'https://docs.google.com/presentation/embed?id=1PE-56ZA-Ngm-exuqYLiDR0H19pLXgxK4SzkaKzaJCls&slide='
current = 1
total = 0

page = urllib.request.urlopen(url).read()
bs = BeautifulSoup(page)
print(bs.find(id=':s'))
#sys.exit(0)

def check():
  global current
  Timer(0.1, check).start()
  print('check')
  if os.path.exists('/root/slidemaster/NEXT'):
    os.remove('/root/slidemaster/NEXT')
    print('Next slide')
  elif os.path.exists('/root/slidemaster/PREVIOUS'):
    os.remove('/root/slidemaster/PREVIOUS')
    print('Previous slide')

def create():
  Timer(0.5, create).start()
  os.system('touch /root/slidemaster/NEXT')

@route('/')
def hello():
  return """<!DOCTYPE html>
<html>
  <head>
    <title>Test</title>
    <style type="text/css">
    html, body {
      margin: 0;
      padding: 0;
      height: 100%;
      overflow: hidden;
    }

    #content {
      position: absolute;
      left: 0;
      right: 0;
      bottom: 0;
      top: 0;
    }

    #frame {
      border: 0;
      width: 100%;
      height: 100%;
    }
    </style>
  </head>
  <body>
    <div id="content">
      <iframe id="frame" src=\"""" + url + """3\"></iframe>
    </div>
  </body>
</html>"""

create()
check()
run(host='104.131.83.142', port=80, debug=True)
