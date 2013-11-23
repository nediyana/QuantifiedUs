'use strict';

describe('Controller: GeoloctimemapCtrl', function () {

  // load the controller's module
  beforeEach(module('frontEndApp'));

  var GeoloctimemapCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    GeoloctimemapCtrl = $controller('GeoloctimemapCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
