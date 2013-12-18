'use strict';

angular.module('prototypeApp')
  .directive('activityStats', function (ActivityStats) {
    return {
      template: '<div></div>',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        ActivityStats.get().then(function(res){
          var data = res.data;
          console.log(data);
          var results = d3.select(element[0]).append('div');
          for(var c in data) {
            var category = data[c],
                name = category.name,
                avg = category.avgDuration,
                median = category.medianDuration,
                totalDuration = category.totalDuration;
            console.log(name);

            results.append('h2').text('Category ' + name);
            results.append('p').text('Average duration: ' + avg);
            results.append('p').text('Median duration: ' + median);
            results.append('p').text('Total duration: ' + totalDuration);
          }

        });
      }
    };
  });
