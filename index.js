var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var path = require('path');

app.get('/', function(req, res){
  res.sendFile(path.join(__dirname, '../slidemaster', 'index.html'));
});

var slidenum = 1;
io.on('connection', function(socket){
  console.log('a user connected, slide: ' + slidenum);
  io.emit('slide', slidenum);
  socket.on('slide', function(num){
    slidenum = num;
    io.emit('slide', num);
    console.log('new slide: ' + num);
  });

  socket.on('disconnect', function() {
    console.log('user disconnected');
  });
});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
