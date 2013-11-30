'use strict';

describe('Service: Activitydata', function () {

  // load the service's module
  beforeEach(module('PrototypeApp'));

  // instantiate service
  var Activitydata;
  beforeEach(inject(function (_Activitydata_) {
    Activitydata = _Activitydata_;
  }));

  it('should do something', function () {
    expect(!!Activitydata).toBe(true);
  });

});
