from bottle import route, run, request
from bs4 import BeautifulSoup
import urllib
import sys

url = 'https://docs.google.com/presentation/embed?id=1PE-56ZA-Ngm-exuqYLiDR0H19pLXgxK4SzkaKzaJCls&slide='
current = 1
total = 0

page = urllib.request.urlopen(url).read()
bs = BeautifulSoup(page)
#print(bs.prettify())
#sys.exit(0)

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

run(host='104.131.83.142', port=80, debug=True)
