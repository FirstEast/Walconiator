/////////////////////////
/// SETUP PARAMETERS ///
////////////////////////

//client username
var user="user";
//client password
var pass="pass";

//client & mailserver admin username
var adminUser="user";
//client & mailserver admin password
var adminPass="pass";

//Walconiator port
port=1600;
//mailServer port
var mailPort=1601;


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
http.listen(port, function(){
  console.log('listening on *:'+port.toString());
});

//processor for data from parsed emails that sends useful data to socket update group.
var messageHandler=require('./messageHandler')(io);

//sets up mail server for receiving and parsing emails. Forwards them to handler.
var mailServer=require('./mailServer')(mailPort,adminUser,adminPass,messageHandler);
