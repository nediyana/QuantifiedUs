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
          var map = svg.append('g');

          map.selectAll('g')
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
          var locCircles = map.append('g').selectAll('circle')
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

        }); // end data request
      }
    };
  });
