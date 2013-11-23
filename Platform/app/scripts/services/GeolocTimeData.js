'use strict';

angular.module('prototypeApp')
  .factory('GeolocTimeData', function ($http) {
    return {
      get: function (params) {
        return $http.get('/b', {
          params : params
        });
      }
    };
  });
