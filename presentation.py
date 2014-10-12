from bottle import route, run, request
import http.client
import urllib
import sys
import os
from threading import Timer

presentations = {}

def retrieve_from_options(key):
    with open('options.txt', 'r+') as f:
        for line in f.readlines():
            lineKey = line.split(' = ')[0]
            lineValue = line.split(' = ')[1].replace('\n', '')
            if lineKey == key:
                if lineValue != 'XXXXXXXXXX':
                    return lineValue
    return None

def url(uid, slide=''):
  return 'http://docs.google.com/presentation/embed?id=%s&slide=%s' % (presentations[uid][0], slide)

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
      }
      var current = """ + presentations[request.query['uid']][1] + """;
      setInterval(
        function() {
          $.ajax({
            url: 'http://sm.aplo.io/?uid=""" + request.query['uid'] + """',
            cache: false,
            dataType: 'html',
            success: function(data) {
              var actual = data.slice(-1);
              if (actual != current) {
                current = actual;
                $("#content").prepend("<iframe id='loading' class='frame' src='""" + url(request.query['uid']) + """\" + current + \"' allowfullscreen='true' onload='unhide();'></iframe>");
              }
            }
          });
        },
      500);
    </script>
  </head>
  <body>
    <div id="content">
      <iframe class="frame" src=\"""" + url(request.query['uid'], presentations[request.query['uid']][1]) + """\" allowfullscreen="true"></iframe>
    </div>
  </body>
</html>""" + presentations[request.query['uid']][1]

@route('/page')
def page():
  presentations[request.query['uid']] = [presentations[request.query['uid']][0], request.query['page']]

@route('/files')
def files():
  connection = http.client.HTTPSConnection('www.googleapis.com', 443, timeout = 30)
  headers = {"Authorization":"Bearer %s" % retrieve_from_options('api_token')}
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
  presentations[uid] = [sid, '1']

run(host='104.131.83.142', port=80, debug=True)
