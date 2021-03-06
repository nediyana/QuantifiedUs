'use strict';

angular.module('prototypeApp')
  .directive('geolocTimeMap', function (GeolocTimeData) {
    // constants

    var height = 500,
        origin = [-122.33, 47.65], // seatle: -122.33, 47.65; pvd: -71.42, 41.83
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
              .scale((1 << 22) / 2 / Math.PI)
              .translate([width / 2, height / 2]);

          var tilePath = d3.geo.path()
              .projection(projection);

          // Append all the map core features like roads, lakes, etc.
          var map = d3.select(element[0]).append('div')
              .attr('class', 'map')
              .style('width', width + 'px')
              .style('height', height + 'px')
              .on('mousemove', mousemoved);

          // The info div houses mouse over latlon coordinate text
          var info = d3.select(element[0]).append('div')
              .attr('class', 'info')
              .style('min-height', '20px');

          // The SVG that contains all layers of the map
          var mapSvg = map.append('svg'),
              mapLayer = mapSvg.append('g').attr('class', 'mapLayer'),
              ptsLayer = mapSvg.append('g').attr('class', 'ptsLayer');

          mapLayer.style({'height': height+'px', 'width': width+'px', 'z-index': -1000});

          ptsLayer.style({'height': height+'px', 'width': width+'px', 'z-index': 1});

          // Append map primitive paths (e.g., water, roads, etc.)
          // drawMap() is the function for drawing a static map
          function drawMap(image) {
            image.selectAll('g')
              .data(tiler
                .scale(projection.scale() * 2 * Math.PI)
                .translate(projection([0, 0])))
              .enter().append('g')
              .each(function(d) {
                var g = d3.select(this);
                this._xhrWaterTiles = d3.json('http://' + ['a', 'b', 'c'][(d[0]* 31 + d[1]) % 3] +
                    '.tile.openstreetmap.us/vectiles-water-areas/' + d[2] + '/' + d[0] + '/' + d[1]
                    + '.json', function(error, json) {
                  g.append('g').selectAll('path')
                    .data(json.features.sort(function(a, b) { return a.properties.sort_key -
                        b.properties.sort_key; }))
                    .enter().append('path')
                    .attr('class', 'water')
                    .attr('d', tilePath);
                });
                this._xhrTiles = d3.json('http://' + ['a', 'b', 'c'][(d[0] * 31 + d[1]) % 3] +
                    '.tile.openstreetmap.us/vectiles-highroad/' + d[2] + '/' + d[0] + '/' + d[1] +
                    '.json', function(error, json) {
                  g.append('g').selectAll('path')
                    .data(json.features.sort(function(a, b) { return a.properties.sort_key -
                        b.properties.sort_key; }))
                    .enter().append('path')
                    .attr('class', function(d) { return d.properties.kind; })
                    .attr('d', tilePath);
                });
              });
          }

          function drawTiledMap(image) {
            console.log('drawTiledMap()');
            // image.append('rect').attr('width', 100).attr('height', 100)
            //     .style({'width': 100, 'height': 100, 'fill': 'red'});

            var map = image.enter().append("g")
                .attr("class", "tile")
                .style("left", function(d) { return 0;console.log(d[0]);return d[0] * 256 + "px"; })
                .style("top", function(d) { return 0; console.log(d[1]);return d[1] * 256 + "px"; })
                .each(function(d) {
                  var svg = d3.select(this);
                  this._xhr = d3.json("http://" + ["a", "b", "c"][(d[0] * 31 + d[1]) % 3] + ".tile.openstreetmap.us/vectiles-highroad/" + d[2] + "/" + d[0] + "/" + d[1] + ".json", function(error, json) {
                    var k = Math.pow(2, d[2]) * 256; // size of the world in pixels

                    tilePath.projection()
                        .translate(projection(origin))//[k / 2 - d[0] * 256, k / 2 - d[1] * 256]) // [0°,0°] in pixels
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
              .translate(projection(origin))//projection([-71.42, 41.83]))//.map(function(x) { console.log(x); return -x; }))
              .on('zoom', zoomFn);
          // projection
          //   .scale(1 / 2 / Math.PI)
          //   .translate([0, 0]);
          //map.call(zoom);


          function zoomFn() {
            var mapTiles = tiler.scale(zoom.scale())
                .translate(zoom.translate())
                ();
            projection
                .scale(zoom.scale() / 2 / Math.PI)
                .translate(zoom.translate());

            var image = mapLayer//.style(transPrefix + 'transform', matrix3d(mapTiles.scale, mapTiles.translate))
              .selectAll('.tile')
                .data(mapTiles, function(d) { return d; });

            image.exit()
                .each(function(d) {
                  this._xhr.abort();
                  this._xhrWater.abort();
                })
                .remove();
            console.log(image.data());
            console.log('----');

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



        ////////////////////////////////
        // BRUSHING

          // Timeline and brushing support
          // Inspired by http://bl.ocks.org/mbostock/4349545
          var dates = data.map(function(d) { return d.date; }),
              maxDate = new Date(Math.max.apply(null,dates)),
              minDate = new Date(Math.min.apply(null,dates));

          var margin = {top: 0, right: 17, bottom: 75, left: 17},
              brushWidth = 920 - margin.left - margin.right,
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

          var svgBrush = d3.select(element[0]).append("svg")
            .attr("width", 920)
            .style('width', brushWidth+'px')
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
            .attr("r", 3.5)
            .style({'fill': 'rgba(255, 75, 75, .5)', 'stroke': 'rgba(150, 75, 75, .1)'});

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

        // END BRUSHING
        /////////////////////////////////

        }); // end data request
      }, // end link: function postLink() { ... }
    };
  });