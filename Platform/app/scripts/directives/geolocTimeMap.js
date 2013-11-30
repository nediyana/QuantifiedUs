'use strict';

angular.module('prototypeApp')
  .directive('geolocTimeMap', function (GeolocTimeData) {
    // constants

    var height = 500,
        origin = [-71.42, 41.83], // seatle: -122.33, 47.65; pvd: -71.42, 41.83
        width = 900;

    return {
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        GeolocTimeData.get().then(function(res){
          var data = res.data.map(function(d) {
            return {'date': new Date(d.date), 'lat': parseFloat(d.lat), 'lon': parseFloat(d.lon) };
          });
          var svg = d3.select(element[0])
            .append('svg')
              .attr('height', height)
              .attr('width', width);

          // Map setup
          var tiler = d3.geo.tile()
              .size([width, height]);

          var projection = d3.geo.mercator()
              .center(origin)
              .scale((1 << 16) / 2 / Math.PI)
              .translate([width / 2, height / 2]);

          var path = d3.geo.path()
              .projection(projection);

          // Append all the map core features like roads, lakes, etc.
          svg.append('g').selectAll('g')
              .data(tiler
                .scale(projection.scale() * 2 * Math.PI)
                .translate(projection([0, 0])))
              .enter().append('g')
              .each(function(d) {
                var g = d3.select(this);
                d3.json('http://' + ['a', 'b', 'c'][(d[0] * 31 + d[1]) % 3] + '.tile.openstreetmap.us/vectiles-water-areas/' + d[2] + '/' + d[0] + '/' + d[1] + '.json', function(error, json) {
                g.append('g').selectAll('path')
                  .data(json.features.sort(function(a, b) { return a.properties.sort_key - b.properties.sort_key; }))
                  .enter().append('path')
                  .attr('class', 'water')
                  .attr('d', path);
                });
                d3.json('http://' + ['a', 'b', 'c'][(d[0] * 31 + d[1]) % 3] + '.tile.openstreetmap.us/vectiles-highroad/' + d[2] + '/' + d[0] + '/' + d[1] + '.json', function(error, json) {
                g.append('g').selectAll('path')
                  .data(json.features.sort(function(a, b) { return a.properties.sort_key - b.properties.sort_key; }))
                  .enter().append('path')
                  .attr('class', function(d) { return d.properties.kind; })
                  .attr('d', path);
                });
              });

          // Append the points from data
          var locCircles = svg.append('g').selectAll('circle')
            .data(data)
            .enter()
              .append('circle')
                .attr('cx', function(d) {
                  return projection([d.lon,d.lat])[0];
                })
                .attr('cy', function(d) {
                  return projection([d.lon,d.lat])[1];
                })
                .attr('r', 3)
                .attr('fill', 'rgba(50,200,50,1');

          // Timeline and brushing support
          // Inspired by http://bl.ocks.org/mbostock/4349545
          var dates = data.map(function(d) { return d.date; }),
              maxDate = new Date(Math.max.apply(null,dates)),
              minDate = new Date(Math.min.apply(null,dates));

          var margin = {top: 0, right: 17, bottom: 75, left: 17},
              brushWidth = 900 - margin.left - margin.right,
              brushHeight = 100 - margin.top - margin.bottom;

          var dateX = d3.time.scale()
              .domain([minDate, maxDate])
              .range([0, brushWidth]);

          var brush = d3.svg.brush()
            .x(dateX)
            .extent([.3, .5])
            .on("brushstart", brushstart)
            .on("brush", brushmove)
            .on("brushend", brushend);

          var arc = d3.svg.arc()
            .outerRadius(brushHeight / 4)
            .startAngle(0)
            .endAngle(function(d, i) { return i ? -Math.PI : Math.PI; });

          var svgBrush = d3.select("body").append("svg")
            .attr("width", brushWidth + margin.left + margin.right)
            .attr("height", brushHeight + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

          svgBrush.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + brushHeight + ")")
            .call(d3.svg.axis().scale(dateX).orient("bottom"));

          var circle = svgBrush.append("g").selectAll("circle")
            .data(data)
          .enter().append("circle")
            .attr("transform", function(d) { return "translate(" + dateX(d.date) + "," + brushHeight/2 + ")"; })
            .attr("r", 3.5);

          var brushg = svgBrush.append("g")
            .attr("class", "brush")
            .call(brush);

          brushg.selectAll(".resize").append("path")
            .attr("transform", "translate(0," +  brushHeight / 2 + ")")
            .attr("d", arc);

          brushg.selectAll("rect")
            .attr("height", brushHeight);

          brushstart();
          brushmove();

          function brushstart() {
            svgBrush.classed("selecting", true);
          }

          function brushmove() {
            var s = brush.extent();
            circle.classed('selected', function(d) { return s[0] <= d.date && d.date <= s[1]; });
            locCircles.classed('selectedGeoLoc',  function(d) {
              return s[0] <= d.date && d.date <= s[1];
            });
            locCircles.classed('notSelectedGeoLoc', function(d) {
              return !(s[0] <= d.date && d.date <= s[1]);
            });
          }

          function brushend() {
            svgBrush.classed("selecting", !d3.event.target.empty());
          }
        });
      }
    };
  });
