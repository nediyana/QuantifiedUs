'use strict';

describe('Service: Geoloctimedata', function () {

  // load the service's module
  beforeEach(module('PrototypeApp'));

  // instantiate service
  var Geoloctimedata;
  beforeEach(inject(function (_Geoloctimedata_) {
    Geoloctimedata = _Geoloctimedata_;
  }));

  it('should do something', function () {
    expect(!!Geoloctimedata).toBe(true);
  });

});
