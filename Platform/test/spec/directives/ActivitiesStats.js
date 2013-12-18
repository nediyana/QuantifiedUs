'use strict';

describe('Directive: activitiesStats', function () {

  // load the directive's module
  beforeEach(module('prototypeApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<activities-stats></activities-stats>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the activitiesStats directive');
  }));
});
