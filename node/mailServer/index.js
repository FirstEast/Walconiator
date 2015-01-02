var mailserver = function(serverPort,adminUser,adminPass,handler){ 
    var mailin = require('mailin');
    mailin.start({
      port: serverPort,
      disableWebhook: true // Disable the webhook posting.
    });

    /* Access simplesmtp server instance. */
    mailin.on('authorizeUser', function(connection, username, password, done) {
      if (username === adminUser && password === adminPass) {
        done(null, true);
      } else {
        done(new Error("Unauthorized!"), false);
      }
      console.log('lol');
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
      /* Do something useful with the parsed message here.
       * Use parsed message `data` directly or use raw message `content`. */
       console.log(data);
       handler.handle(data);
    });
}

module.exports=mailserver;
