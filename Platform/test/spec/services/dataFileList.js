'use strict';

describe('Service: Datafilelist', function () {

  // load the service's module
  beforeEach(module('UpdateApp'));

  // instantiate service
  var Datafilelist;
  beforeEach(inject(function (_Datafilelist_) {
    Datafilelist = _Datafilelist_;
  }));

  it('should do something', function () {
    expect(!!Datafilelist).toBe(true);
  });

});
