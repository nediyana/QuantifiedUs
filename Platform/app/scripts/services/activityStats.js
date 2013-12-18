'use strict';

angular.module('prototypeApp')
  .factory('ActivityStats', function ($http) {
    return {
      get: function (params) {
        return $http.get('/activityStats', {
          params : params
        });
      }
    };
  });
