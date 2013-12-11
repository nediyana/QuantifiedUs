/* global require:true, console:true, process:true, __dirname:true */
'use strict'

var express     = require('express'),
    fs          = require('fs'),
    http        = require('http'),
    port        = process.argv[2] || 8002;

// Server setup
var app = express();
app.use(express.bodyParser());
app.use(express.static(__dirname + '/app'));

app.get('/geolocTimeData', function(req, res) {
  res.sendfile('data/locations.json');
});

app.get('/activityData', function(req, res) {
  res.sendfile('data/sampleActivity_daily.json');
});

app.get('/dataFileList', function(req, res) {
  fs.readdir('data', function(err, files) {
    if (err) throw err;
    console.log('data files: ' + files);
    var jsons = files.filter(function(f) {
      return f.indexOf('.json') != -1;
    })
    console.log(jsons);
    res.send(jsons);
  });
  console.log('data file list requested');
});

// Create the server and tell which port to listen to
http.createServer(app).listen(port, function (err) {
  if (!err) console.log('Listening on port ' + port);
});
