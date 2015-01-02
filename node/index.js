/////////////////////////
/// SETUP PARAMETERS ///
////////////////////////

//client username
user="user";
//client password
pass="pass";

//admin username
adminUser="user";
//admin password
adminPass="pass";

//WALCONIATOR CLIENT SERVER
var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var path = require('path');

//sends webpages
app.set('views', path.join(__dirname, 'views'));
app.use(express.static(path.join(__dirname, 'public')));
require('./routes')(app);

//adds valid clients to group for mail posting updates
io.on('connection', function(socket){
  socket.emit('connected',true);
  socket.on('login',function(msg){
      if(msg.user===user && msg.pass=pass){
        socket.join('walconia');
        socket.emit('login',true);
      }
      else if(msg.user===adminUser && msg.pass=adminPass){
        socket.join('walconiator');
        socket.emit('login',true);
      }
      else{
        socket.emit('login',false);
      }
  });
});
http.listen(1600, function(){
  console.log('listening on *:1600');
});

//processor for data from parsed emails that sends useful data to socket update group.
var messageHandler=require('./messageHandler')(io);

//sets up mail server for receiving and parsing emails. Forwards them to handler.
var mailServer=require('./mailServer')(adminUser,adminPass,messageHandler);
