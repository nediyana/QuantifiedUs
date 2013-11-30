'use strict';

angular.module('prototypeApp')
  .controller('MainCtrl', function ($scope) {
    $scope.navList = [
      { 'name': 'Geolocation Points', 'url':'/#/geolocTimeMap' },
      { 'name': 'Activity Stackchart', 'url':'/#/activityStackchart'}
    ];
  });
