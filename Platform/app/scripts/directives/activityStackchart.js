'use strict';

angular.module('prototypeApp')
  .directive('activityStackchart', function (ActivityData) {
    return {
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        function formatData(data) {
          data.forEach(function(d) {
            var values = d['values'];
            values.forEach(function(v) {
              var formatDate = d3.time.format("%Y-%m-%d"),
                  formatTime = d3.time.format("%H:%M:%S");

              // Convert date into a Date object
              v[0] = formatDate.parse(v[0]);

              // Convert duration into seconds
              var duration = formatTime.parse(v[1]);
              v[1] = duration.getHours()*360 + duration.getMinutes()*60 + duration.getSeconds();
            });
          });
          return data;
        }


        element.text('this is the activityStackchart directive');
        ActivityData.get().then(function(res){
          var data = formatData(res.data);
          console.log(data);

          nv.addGraph(function() {
            var chart = nv.models.stackedAreaChart()
                          .x(function(d) { return d[0] })
                          .y(function(d) { return d[1] })
                          .clipEdge(true);

            chart.xAxis
                .tickFormat(function(d) { return d3.time.format('%x')(new Date(d)) });

            // chart.yAxis
            //     .tickFormat(d3.format(',.2f'));

            d3.select(element[0])
              .append('svg')
                .attr('width', 500)
              .datum(data)
                .transition().duration(500).call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
          });
        }); // end response code
      } // end link
    };
  });
