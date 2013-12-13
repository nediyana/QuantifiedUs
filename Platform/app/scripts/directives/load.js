'use strict';

angular.module('prototypeApp')
  .directive('load', function (DataFileList) {
    return {
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        console.log('loaded');
        DataFileList.get().then(function(res){
          var data = res.data;
          console.log(data);

          var elem = d3.select(element[0]).append('div');

          elem.append('h1').text('Files');
          var fileTable = elem.append('table').attr('class','fileList table table-striped');
          var fileTableHead = fileTable.append('thead')
            .append('tr');
          fileTableHead.append('th').text('File Name');
          fileTableHead.append('th').text('Visualization')

          var fileTableRows = fileTable
            .append('tbody')
            .selectAll('tr')
            .data(data)
            .enter()
            .append('tr');

          fileTableRows
            .append('td').text(function(d) { return d; });
          fileTableRows
            .append('td')
            .append('select')
              .selectAll('option')
              .data([ {k:'none', v:'Do not use'},
                      {k:'activity', v:'Activity Stacked Linechart'},
                      {k: 'geoloc', v:'Geolocation Plotted Map'}])
              .enter()
              .append('option')
                .attr('value', function(d) { return d.k; })
                .text(function(d){ return d.v; });

          // var el = $compile('<geoloc-time-map val="data"></geoloc-time-map>')($scope);
          var loadBtn = elem.append('button')
              .attr('class', 'btn btn-primary')
              .text('Load data')
              .on('click', function(){
                // elem.node().append(el);
              });
        });
      }
    };
  });
