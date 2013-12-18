'use strict';

angular.module('prototypeApp', [
  'ngCookies',
  'ngResource',
  'ngSanitize'
])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
      })
      .when('/activityStackchart', {
        templateUrl: 'views/activityStackchart.html',
        controller: 'ActivityStackchartCtrl'
      })
      .when('/geolocTimeMap', {
        templateUrl: 'views/geolocTimeMap.html',
        controller: 'GeolocTimeMapCtrl'
      })
      .when('/launch', {
        templateUrl: 'views/launch.html',
        controller: 'LaunchCtrl'
      })
      .when('/loadData', {
        templateUrl: 'views/load.html',
        controller: 'LoadDataCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
