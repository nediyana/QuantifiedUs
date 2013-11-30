'use strict';

describe('Directive: activityStackchart', function () {

  // load the directive's module
  beforeEach(module('prototypeApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<activity-stackchart></activity-stackchart>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the activityStackchart directive');
  }));
});
