from bottle import route, run, request
import http.client
import urllib
import sys
import os
from threading import Timer

current = 1
presentations = {}

def url(uid, slide):
  return 'http://docs.google.com/presentation/embed?id=%s&slide=%s' % (presentations[uid], slide)

def check():
  global current
  Timer(0.1, check).start()
  if os.path.exists('/root/slidemaster/NEXT'):
    os.remove('/root/slidemaster/NEXT')
    current += 1
    print('Slide %s' % current)
  elif os.path.exists('/root/slidemaster/PREVIOUS'):
    os.remove('/root/slidemaster/PREVIOUS')
    current -= 1
    print('Previous slide %s' % current)

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

    .frame {
      border: 0;
      width: 100%;
      height: 100%;
    }

    #loading {
      display: none;
    }
    </style>
    <script src="http://code.jquery.com/jquery-2.1.1.min.js" type="text/javascript"></script>
    <script src="http://bililite.com/inc/jquery.sendkeys.js" type="text/javascript"></script>
    <script src="http://bililite.com/inc/bililiteRange.js" type="text/javascript"></script>
    <script type="text/javascript">
      function unhide() {
        $("#loading").removeAttr('id');
        console.log('unhid');
      }
      var current = """ + str(current) + """;
      setInterval(
        function() {
          $.ajax({
            url: 'http://sm.aplo.io/',
            cache: false,
            dataType: 'html',
            success: function(data) {
              var actual = data.slice(-1);
              if (actual != current) {
                current = actual;
                //current = actual;
                //console.log(actual);
                $("#content").prepend("<iframe id='loading' class='frame' src='""" + url(request.query['uid'], str(current)) + """\" + current + \"' allowfullscreen='true' onload='unhide();'></iframe>");
              }
            }
          });
        },
      500);
    </script>
  </head>
  <body>
    <div id="content">
      <iframe class="frame" src=\"""" + url(request.query['uid'], str(current)) + """\" allowfullscreen="true"></iframe>
    </div>
  </body>
</html>""" + str(current)

@route('/next')
def next():
  os.system('touch /root/slidemaster/NEXT')

@route('/previous')
def previous():
  os.system('touch /root/slidemaster/PREVIOUS')

@route('/files')
def files():
  connection = http.client.HTTPSConnection('www.googleapis.com', 443, timeout = 30)
  headers = {"Authorization":"Bearer ya29.nABnpZBILnU65PKjF42M9sbDZekIhGrj5JfvmtJNnlzBXjXMgARpN_Kb"}
  connection.request('GET', '/drive/v2/files', None, headers)
  try:
    response = connection.getresponse()
    content = response.read()
    return content
  except:
    print('Exception during request')

@route('/create')
def create():
  uid = request.query['uid']
  sid = request.query['sid']
  presentations[uid] = sid

check()
run(host='104.131.83.142', port=80, debug=True)
