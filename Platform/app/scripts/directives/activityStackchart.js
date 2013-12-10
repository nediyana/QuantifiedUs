'use strict';

angular.module('prototypeApp')
  .directive('activityStackchart', function (ActivityData) {
    return {
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        var disabledSeries = [1]
        ActivityData.get().then(function(res){
          console.log(res);
          var dailyData = res.data;
          var colors = d3.scale.category20();
          var keyColor = function(d, i) {return colors(d.key)};

          var chart;
          nv.addGraph(function() {
            chart = nv.models.stackedAreaChart()
                          .useInteractiveGuideline(true)
                          .x(function(d) { return d[0] })
                          .y(function(d) { return d[1] })
                          .margin({top: 30, right: 25, bottom: 50, left: 75})
                          .color(keyColor)
                          .transitionDuration(300);
            chart.yAxis.axisLabel('Hours');
            chart.xAxis.axisLabel('Date');
            chart.xAxis.tickFormat(function(d) { return d3.time.format('%b %e')(new Date((d - 719162) * 24 * 60 * 60 * 1000)) });
            chart.yAxis.tickFormat(function(d) { return Math.floor(d / 60) + ':' + (d % 60 < 10 ? '0' : '') + d % 60; });
            chart.controlsData(['Stacked', 'Expanded']);

            var svg = d3.select(element[0])
            .append('svg')
              .datum(dailyData)
              .style('height', 500)
              .transition().duration(0)
              .call(chart);

            var state = chart.state();
            for(var i=0; i < state.disabled.length; i++) {
              if (i in disabledSeries)
                state.disabled[i] = true;
            }
            chart.dispatch.changeState(state);

            var plotHeight = parseInt(d3.select("rect").attr('height'));

            var dailyToggle = d3.select('svg')
              .append('circle')
              .attr('transform', "translate(" + 92 + "," + (plotHeight + 62) + ")")
              .attr('r', 5)
              .attr('class', 'toggleCircle toggle')
              .style('fill', '#444444');
            var dailyText = d3.select('svg')
              .append('text')
              .text('Daily')
              .attr('class', 'toggle')
              .attr('transform', "translate(" + 100 + "," + (plotHeight + 66) + ")");
            var weeklyToggle = d3.select('svg')
              .append('circle')
              .attr('transform', "translate(" + 152 + "," + (plotHeight + 62) + ")")
              .attr('r', 5)
              .attr('class', 'toggleCircle toggle');
            var weeklyText = d3.select('svg')
              .append('text')
              .text('Weekly')
              .attr('class', 'toggle')
              .attr('transform', "translate(" + 160 + "," + (plotHeight + 66) + ")");

            var toggleDaily = function(d) {
              d3.json(dailyDatafile, function(dailyData) {
                dailyToggle.style('fill', '#444444');
                weeklyToggle.style('fill', 'white');
                d3.select('svg')
                  .datum(dailyData)
                  .transition().duration(0)
                  .call(chart);
                var state = chart.state();
                for(var i=0; i < state.disabled.length; i++) {
                  if (i in disabledSeries)
                    state.disabled[i] = true;
                }
                chart.dispatch.changeState(state);
              });
            };

            dailyToggle.on('click', toggleDaily);
            dailyText.on('click', toggleDaily);

            var toggleWeekly = function(d) {
              d3.json(weeklyDatafile, function(weeklyData) {
                weeklyToggle.style('fill', '#444444');
                dailyToggle.style('fill', 'white');
                d3.select('svg')
                  .datum(weeklyData)
                  .transition().duration(0)
                  .call(chart);
                var state = chart.state();
                for(var i=0; i < state.disabled.length; i++) {
                  if (i in disabledSeries)
                    state.disabled[i] = true;
                }
                chart.dispatch.changeState(state);
              });
            };

            weeklyToggle.on('click', toggleWeekly);
            weeklyText.on('click', toggleWeekly);

            nv.utils.windowResize(chart.update);

            return chart;
          });
        }); // end response code
      } // end link
    };
  });
