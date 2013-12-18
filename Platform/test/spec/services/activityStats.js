'use strict';

describe('Service: Activitystats', function () {

  // load the service's module
  beforeEach(module('PrototypeApp'));

  // instantiate service
  var Activitystats;
  beforeEach(inject(function (_Activitystats_) {
    Activitystats = _Activitystats_;
  }));

  it('should do something', function () {
    expect(!!Activitystats).toBe(true);
  });

});
