'use strict';

angular.module('prototypeApp')
  .factory('ActivityData', function ($http) {
    return {
      get: function (params) {
        return $http.get('/activityData', {
          params : params
        });
      }
    };
  });
