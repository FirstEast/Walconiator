var routes=function(app){
    app.get('/', function(req, res){
      res.sendfile('views/index.html');
    });

    app.get('/admin', function(req, res){
      res.sendfile('views/admin.html');
    });
}

module.exports=routes;