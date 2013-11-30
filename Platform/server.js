/* global require:true, console:true, process:true, __dirname:true */
'use strict'

var express     = require('express'),
    http        = require('http'),
    port        = process.argv[2] || 8002;

// Server setup
var app = express();
app.use(express.bodyParser());
app.use(express.static(__dirname + '/app'));

app.get('/geolocTimeData', function(req, res) {
  res.sendfile('sampleData/locations.json');
});

app.get('/activityData', function(req, res) {
  res.sendfile('sampleData/sampleActivity.json');
});

// Create the server and tell which port to listen to
http.createServer(app).listen(port, function (err) {
  if (!err) console.log('Listening on port ' + port);
});
