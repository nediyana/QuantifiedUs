'use strict';

describe('Directive: geolocTimeMap', function () {

  // load the directive's module
  beforeEach(module('frontEndApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<geoloc-time-map></geoloc-time-map>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the geolocTimeMap directive');
  }));
});
