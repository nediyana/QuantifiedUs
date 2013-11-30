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
      .when('/geolocTimeMap', {
        templateUrl: 'views/geolocTimeMap.html',
        controller: 'GeolocTimeMapCtrl'
      })
      .when('/activityStackchart', {
        templateUrl: 'views/activityStackchart.html',
        controller: 'ActivityStackchartCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
