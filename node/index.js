/////////////////////////
/// SETUP PARAMETERS ///
////////////////////////

//client username
user="user";
//client password
pass="pass";

//admin username
adminUser="user";
adminPass="pass";

//WALCONIATOR SERVER

var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.use(express.static(__dirname + '/public'));

io.on('connection', function(socket){
  socket.emit('connected',true);
  socket.on('login',function(msg){
      if(msg.user===username && msg.pass=password){
        socket.join('walconia');
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


// SMTP MAILSERVER SERVER 
var mailin = require('mailin');

mailin.start({
  port: 25,
  disableWebhook: true // Disable the webhook posting.
});

/* Access simplesmtp server instance. */
mailin.on('authorizeUser', function(connection, username, password, done) {
  if (username == adminUser && password == adminPass) {
    done(null, true);
  } else {
    done(new Error("Unauthorized!"), false);
  }
});

/* Event emitted when a connection with the Mailin smtp server is initiated. */
mailin.on('startMessage', function (connection) {
  /* connection = {
      from: 'sender@somedomain.com',
      to: 'someaddress@yourdomain.com',
      id: 't84h5ugf',
      authentication: { username: null, authenticated: false, status: 'NORMAL' }
    }
  }; */
  console.log(connection);
});

/* Event emitted after a message was received and parsed. */
mailin.on('message', function (connection, data, content) {
  console.log(data);
  /* Do something useful with the parsed message here.
   * Use parsed message `data` directly or use raw message `content`. */
   socket.to("walconia").emit('email',data);
});