'use strict';

describe('Controller: LoaddataCtrl', function () {

  // load the controller's module
  beforeEach(module('updateApp'));

  var LoaddataCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    LoaddataCtrl = $controller('LoaddataCtrl', {
      $scope: scope
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(scope.awesomeThings.length).toBe(3);
  });
});
