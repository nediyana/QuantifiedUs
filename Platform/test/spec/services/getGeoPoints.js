'use strict';

describe('Service: Getgeopoints', function () {

  // load the service's module
  beforeEach(module('PrototypeApp'));

  // instantiate service
  var Getgeopoints;
  beforeEach(inject(function (_Getgeopoints_) {
    Getgeopoints = _Getgeopoints_;
  }));

  it('should do something', function () {
    expect(!!Getgeopoints).toBe(true);
  });

});
