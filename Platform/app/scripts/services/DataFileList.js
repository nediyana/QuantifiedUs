'use strict';

angular.module('prototypeApp')
  .factory('DataFileList', function ($http) {
    return {
      get: function (params) {
        return $http.get('/dataFileList', {
          params : params
        });
      }
    };
  });
