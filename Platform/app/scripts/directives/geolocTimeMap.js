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

          // Utility
          var transPrefix = prefixMatch(["webkit", "ms", "Moz", "O"]);
          function prefixMatch(p) {
            var i = -1, n = p.length, s = document.body.style;
            while (++i < n) if (p[i] + "Transform" in s) return "-" + p[i].toLowerCase() + "-";
            return "";
          }

          // Map setup
          var tiler = d3.geo.tile()
              .size([width, height]);

          var projection = d3.geo.mercator()
              .center(origin)
              .scale((1 << 21) / 2 / Math.PI)
              .translate([width / 2, height / 2]);

          var tilePath = d3.geo.path()
              .projection(projection);

          // Append all the map core features like roads, lakes, etc.
          var map = d3.select(element[0]).append('div')
              .attr('class', 'map')
              .style('width', width + 'px')
              .style('height', height + 'px')
              .on('mousemove', mousemoved);

          var info = d3.select(element[0]).append('div')
              .attr('class', 'info');

          var mapSvg = map.append('svg'),
              mapLayer = mapSvg.append('g').attr('class', 'mapLayer'),
              ptsLayer = mapSvg.append('g').attr('class', 'ptsLayer');

          mapLayer.style({'height': height+'px', 'width': width+'px', 'z-index': -1000});

          ptsLayer.style({'height': height+'px', 'width': width+'px', 'z-index': 1});

          // Append map primitive paths (e.g., water, roads, etc.)
          function drawMap(image) {
            console.log(projection.scale(), zoom.scale());
            image.selectAll('g')
              .data(tiler
                .scale(projection.scale() * 2 * Math.PI)
                .translate(projection([0, 0])))
              .enter().append('g')
              .each(function(d) {
                var g = d3.select(this);
                this._xhrWaterTiles = d3.json('http://' + ['a', 'b', 'c'][(d[0] * 31 + d[1]) % 3] + '.tile.openstreetmap.us/vectiles-water-areas/' + d[2] + '/' + d[0] + '/' + d[1] + '.json', function(error, json) {
                g.append('g').selectAll('path')
                  .data(json.features.sort(function(a, b) { return a.properties.sort_key - b.properties.sort_key; }))
                  .enter().append('path')
                  .attr('class', 'water')
                  .attr('d', tilePath);
                });
                this._xhrTiles = d3.json('http://' + ['a', 'b', 'c'][(d[0] * 31 + d[1]) % 3] + '.tile.openstreetmap.us/vectiles-highroad/' + d[2] + '/' + d[0] + '/' + d[1] + '.json', function(error, json) {
                g.append('g').selectAll('path')
                  .data(json.features.sort(function(a, b) { return a.properties.sort_key - b.properties.sort_key; }))
                  .enter().append('path')
                  .attr('class', function(d) { return d.properties.kind; })
                  .attr('d', tilePath);
                });
              });
          }

          function drawTiledMap(image) {
            var map = image.enter().append("g")
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
          }


          // Zoom code that calls map primitive adding
          var zoom = d3.behavior.zoom()
              .scale(projection.scale() * 2 * Math.PI)
              .scaleExtent([1 << 20, 1 << 23])
              .translate(projection([-71.42, 41.83]).map(function(x) { return -x; }))
              .on('zoom', zoomFn);
          //map.call(zoom);
          function zoomFn() {
            var mapTiles = tiler.scale(zoom.scale())
                .translate(zoom.translate())
                ();
            projection
                .scale(zoom.scale() / 2 / Math.PI)
                .translate(zoom.translate());

            var image = mapLayer.style(transPrefix + 'transform', matrix3d(mapTiles.scale, mapTiles.translate))
              .selectAll('.tile')
                .data(mapTiles, function(d) { return d; });

            image.exit()
                .each(function(d) {
                  this._xhr.abort();
                  this._xhrWater.abort();
                })
                .remove();

            drawTiledMap(image);
          }
          //zoomFn();
          drawMap(mapLayer);

          // Append the points from data
          var locCircles = ptsLayer.append('g').selectAll('circle')
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
                .attr('fill', '#69a139')
                .attr('stroke', '#275a37');

        /////////// Util functions
        function mousemoved() {
            info.text(formatLocation(projection.invert(d3.mouse(this)), projection.scale()));
        }
        function formatLocation(p, k) {
            var format = d3.format("." + Math.floor(Math.log(k) / 2 - 2) + "f");
            return (p[1] < 0 ? format(-p[1]) + "°S" : format(p[1]) + "°N") + " "
                 + (p[0] < 0 ? format(-p[0]) + "°W" : format(p[0]) + "°E");
        }
        function matrix3d(scale, translate) {
          var k = scale / 256, r = scale % 1 ? Number : Math.round;
          return "matrix3d(" + [k, 0, 0, 0, 0, k, 0, 0, 0, 0, k, 0, r(translate[0] * scale), r(translate[1] * scale), 0, 1 ] + ")";
        }

        }); // end data request
      }
    };
  });