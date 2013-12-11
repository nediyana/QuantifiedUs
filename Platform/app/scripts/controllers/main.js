'use strict';

angular.module('prototypeApp')
  .controller('MainCtrl', function ($scope) {
    $scope.navList = [
      { 'name': 'Geolocation Points', 'url':'/#/geolocTimeMap', 'header': 'Geolocation Data',
        'desc': 'Plot your geolocation data on a map, filter through time, and more.' },
      { 'name': 'Activity Stackchart', 'url':'/#/activityStackchart', 'header': 'Activity Data',
        'desc': 'Browse activity log data through visualizations like a stacked line chart, select subsets of data to view, and find out more about your habits.'}
    ];
  });
