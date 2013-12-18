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
  res.sendfile('data/geoLocsSample.json');
});

app.get('/activityStats', function(req, res) {
  var analFile = 'activityStatistics.py',
      args = 'data/activities.json';
  launchScript(analFile, args, function(data) {
    res.send(data);
  });
});

app.get('/activityData', function(req, res) {
  res.sendfile('data/activitySample_daily.json');
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

////////////////////////////////////////////////////////////////////////////////
// Test external launch
function launchScript(fileName, args, callback) {
  var analFile = fileName,
      args = dataPath,
      exec = require('child_process').exec,
      child = exec('python analyses/' + analFile + ' ' + args, function( error, stdout, stderr) {
        if ( error != null ) {
          console.log(stderr);
          // error handling & exit
        }

        callback(JSON.parse(stdout));
      });
  return child;
}

var dataPath = 'data/activities.json',
    fPath = 'activityStatistics.py',
    test = launchScript(fPath, dataPath, function(data) {
      console.log(data);
    });


// Create the server and tell which port to listen to
http.createServer(app).listen(port, function (err) {
  if (!err) console.log('Listening on port ' + port);
});
