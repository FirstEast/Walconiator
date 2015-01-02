var routes=function(app){
    app.get('/', function(req, res){
      res.sendfile('index.html');
    });

    app.get('/admin', function(req, res){
      res.sendfile('admin.html');
    });
}

module.exports=routes;