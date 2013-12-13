# VACUM: Visualizations, Analyses, Conversions, Utilities, and Models

VACUM is a tool for ... built primarily on top of AngularJS and d3.

## Installation
To run VACUM after cloning the repo you must have Node.js (http://nodejs.org/) and Yeoman (http://yeoman.io/) installed.
We also recommend using the AngularJS Generator for Yeoman (https://github.com/yeoman/generator-angular).

From the `prototype` directory, run `npm install && bower install` to install dependencies.

## Running the application
To run the application navigate to `prototype/frontEnd` and type `node server.js`. A new window in your default browser will then show up from which you can navigate through the application.

## Geolocation Features
### Data format expectations
Currently VACUM expects a CSV file with each row having entries in lat, lon, time ordering. An example would be 6.101333, 1.147733,2013-07-22 15:52:43.

# Contribution notes
All files have column counts of either 80 or 100 columns.