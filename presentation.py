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
    current += 1
    print('Next slide')
  elif os.path.exists('/root/slidemaster/PREVIOUS'):
    os.remove('/root/slidemaster/PREVIOUS')
    current -= 1
    print('Previous slide')

@route('/')
def presentation():
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
    <script src="http://code.jquery.com/jquery-2.1.1.min.js" type="text/javascript"></script>
    <script type="text/javascript">
      setInterval(
        function() {
          $.ajax({
            url: 'http://104.131.83.142/',
            cache: false,
            dataType: 'html',
            success: function(data) {
              actual = data.slice(-1);
              current = """ + str(current) + """;
              if (actual != current) {
                location.reload();
              }
            }
          });
        },
      500);
    </script>
  </head>
  <body>
    <div id="content">
      <iframe id="frame" src=\"""" + url + str(current) + """\"></iframe>
    </div>
  </body>
</html>""" + str(current)

@route('/next')
def next():
  os.system('touch /root/slidemaster/NEXT')

@route('/previous')
def previous():
  os.system('touch /root/slidemaster/PREVIOUS')

check()
run(host='104.131.83.142', port=80, debug=True)
