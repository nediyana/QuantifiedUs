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
            return {'date': new Date(d.date), 'lat': parseFloat(d.lat), 'lon': -1*parseFloat(d.lon) };
          });

          var prefix = prefixMatch(["webkit", "ms", "Moz", "O"]);
          function prefixMatch(p) {
            var i = -1, n = p.length, s = document.body.style;
            while (++i < n) if (p[i] + "Transform" in s) return "-" + p[i].toLowerCase() + "-";
            return "";
          }

          // Map setup
          var tile = d3.geo.tile()
              .size([width, height]);

          // var projection = d3.geo.mercator()
          //     // .center(origin)
          //     .scale((1 << 16) / 2 / Math.PI)
          //     .translate([width / 2, height / 2]);

          var projection = d3.geo.mercator()
              .scale((1 << 21) / 2 / Math.PI)
              .translate([width / 2, height / 2]);

          var tileProjection = d3.geo.mercator();

          var tilePath = d3.geo.path()
              .projection(tileProjection);

          var zoom = d3.behavior.zoom()
              .scale(projection.scale() * 2 * Math.PI)
              .scaleExtent([1 << 20, 1 << 23])
              .translate(projection([-71.42, 41.83]).map(function(x) { return -x; }))
              .on('zoom', zoomed);

          var map = d3.select(element[0]).append('div')
              .attr('class', 'map')
              .style('width', width + 'px')
              .style('height', height + 'px')
              .call(zoom)
              .on('mousemove', mousemoved);

          var layer = map.append('div')
              .attr('class', 'layer');

          var info = map.append('div')
              .attr('class', 'info');

          // locations is a layer of the map
          // this needs to be refreshed on each zoom/pan event
          var locations = map.append('svg')
            .attr('id', 'blaaaah')
            .attr('width', width)
            .attr('height', height);
          locations
            .append('rect')
              .attr('x', tileProjection([data[0].lat, data[0].lon])[0])
              .attr('y', tileProjection([data[0].lat, data[0].lon])[1]/2)
              .attr('width', 300)
              .attr('height', 300)
              .style('fill', '#000');
          locations.selectAll('circle')
              .data([[41.75897, 71.27580]])
              .enter()
              .append('circle')
              .attr('cx', function(d) {
                return tileProjection(d[0], d[1])[0];
              })
              .attr('cy', function(d) {
                return tileProjection(d[0], d[1])[1];
              })
              .attr('r', 25)
              .attr('fill', 'green');



          zoomed();

          function zoomed() {
            var tiles = tile
                .scale(zoom.scale())
                .translate(zoom.translate())
                ();

            projection
                .scale(zoom.scale() / 2 / Math.PI)
                .translate(zoom.translate());

            var image = layer
                .style(prefix + "transform", matrix3d(tiles.scale, tiles.translate))
              .selectAll(".tile")
                .data(tiles, function(d) { return d; });

            image.exit()
                .each(function(d) {
                  this._xhr.abort();
                  this._xhrWater.abort();
                })
                .remove();

            var map = image.enter().append("svg")
                .attr("class", "tile")
                .style("left", function(d) { return d[0] * 256 + "px"; })
                .style("top", function(d) { return d[1] * 256 + "px"; })
                .each(function(d) {
                  var svg = d3.select(this);
                  this._xhr = d3.json("http://" + ["a", "b", "c"][(d[0] * 31 + d[1]) % 3] + ".tile.openstreetmap.us/vectiles-highroad/" + d[2] + "/" + d[0] + "/" + d[1] + ".json", function(error, json) {
                    var k = Math.pow(2, d[2]) * 256; // size of the world in pixels

                    tilePath.projection()
                        .translate([k / 2 - d[0] * 256, k / 2 - d[1] * 256]) // [0°,0°] in pixels
                        .scale(k / 2 / Math.PI);

                    svg.append('g').selectAll("path")
                        .data(json.features.sort(function(a, b) { return a.properties.sort_key - b.properties.sort_key; }))
                      .enter().append("path")
                        .attr("class", function(d) { return d.properties.kind; })
                        .attr("d", tilePath);
                  });
                  this._xhrWater = d3.json("http://" + ["a", "b", "c"][(d[0] * 31 + d[1]) % 3] + ".tile.openstreetmap.us/vectiles-water-areas/" + d[2] + "/" + d[0] + "/" + d[1] + ".json", function(error, json) {
                    var k = Math.pow(2, d[2]) * 256; // size of the world in pixels

                    tilePath.projection()
                        .translate([k / 2 - d[0] * 256, k / 2 - d[1] * 256]) // [0°,0°] in pixels
                        .scale(k / 2 / Math.PI);

                    svg.append('g').selectAll("path")
                        .data(json.features.sort(function(a, b) { return a.properties.sort_key - b.properties.sort_key; }))
                        .enter().append("path")
                        .attr("class", "water")
                        .attr("d", tilePath)
                        .style({'fill': 'ccccff', 'stroke': 'none'});
                  });
                });
          } // end zoomed()


          function mousemoved() {
            info.text(formatLocation(projection.invert(d3.mouse(this)), zoom.scale()));
          }


          function matrix3d(scale, translate) {
            var k = scale / 256, r = scale % 1 ? Number : Math.round;
            return "matrix3d(" + [k, 0, 0, 0, 0, k, 0, 0, 0, 0, k, 0, r(translate[0] * scale), r(translate[1] * scale), 0, 1 ] + ")";
          }


          function prefixMatch(p) {
            var i = -1, n = p.length, s = document.body.style;
            while (++i < n) if (p[i] + "Transform" in s) return "-" + p[i].toLowerCase() + "-";
            return "";
          }


          function formatLocation(p, k) {
            var format = d3.format("." + Math.floor(Math.log(k) / 2 - 2) + "f");
            return (p[1] < 0 ? format(-p[1]) + "°S" : format(p[1]) + "°N") + " "
                 + (p[0] < 0 ? format(-p[0]) + "°W" : format(p[0]) + "°E");
          }
        }); // end data request
      }
    };
  });
