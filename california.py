// California — 36 timesteps (paper methodology)
var geometry = ee.Geometry.Rectangle([-122.5, 36.0, -119.0, 39.0]);
var BANDS = ['B2','B3','B4','B5','B6','B7','B8','B8A','B11','B12'];

var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterDate('2021-01-01', '2021-12-31')
  .filterBounds(geometry)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
  .select(BANDS);
  

print('Total S2 scenes:', s2.size());

// Build 36 composites — one every 10 days
var timesteps = ee.List.sequence(0, 35);

var compositeList = timesteps.map(function(i) {
  var start = ee.Date('2021-01-01').advance(ee.Number(i).multiply(10), 'day');
  var end   = start.advance(10, 'day');
  var comp  = s2.filterDate(start, end).median().toFloat();
  var empty = ee.Image.constant([0,0,0,0,0,0,0,0,0,0])
                .rename(BANDS).toFloat();
  var hasData = s2.filterDate(start, end).size().gt(0);
  return ee.Image(ee.Algorithms.If(hasData, comp, empty));
});

// Convert list to ImageCollection then stack into one image
var stacked = ee.ImageCollection(compositeList).toBands();
print('Total bands in stacked image:', stacked.bandNames().size());

// CDL labels — no WorldCover mask
var cdl = ee.ImageCollection('USDA/NASS/CDL')
  .filterDate('2021-01-01','2021-12-31')
  .first().select('cropland').clip(geometry);

// 10,000 random points
var points = ee.FeatureCollection.randomPoints(geometry, 10000, 42);

// Attach crop labels
var labeled = cdl.sampleRegions({
  collection: points,
  scale: 30,
  geometries: true
});

print('Labeled points:', labeled.size());

// Attach 360 spectral features (36 timesteps x 10 bands)
var dataset = stacked.sampleRegions({
  collection: labeled,
  scale: 20,
  geometries: false
});

Export.table.toDrive({
  collection: dataset,
  description: 'MCTNet_California_2021_36t',
  fileFormat: 'CSV'
});

print('Done — go to Tasks tab and click RUN');





#------------------- Arkansas
// Arkansas — 36 timesteps
var geometry = ee.Geometry.Rectangle([-91.8, 33.8, -90.2, 35.2]);
var BANDS = ['B2','B3','B4','B5','B6','B7','B8','B8A','B11','B12'];

var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterDate('2021-01-01', '2021-12-31')
  .filterBounds(geometry)
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
  .select(BANDS);

print('Total S2 scenes:', s2.size());

var timesteps = ee.List.sequence(0, 35);
var compositeList = timesteps.map(function(i) {
  var start = ee.Date('2021-01-01').advance(ee.Number(i).multiply(10), 'day');
  var end   = start.advance(10, 'day');
  var comp  = s2.filterDate(start, end).median().toFloat();
  var empty = ee.Image.constant([0,0,0,0,0,0,0,0,0,0])
                .rename(BANDS).toFloat();
  var hasData = s2.filterDate(start, end).size().gt(0);
  return ee.Image(ee.Algorithms.If(hasData, comp, empty));
});

var stacked = ee.ImageCollection(compositeList).toBands();
print('Total bands:', stacked.bandNames().size());

var cdl = ee.ImageCollection('USDA/NASS/CDL')
  .filterDate('2021-01-01','2021-12-31')
  .first().select('cropland').clip(geometry);

var points = ee.FeatureCollection.randomPoints(geometry, 10000, 42);

var labeled = cdl.sampleRegions({
  collection: points,
  scale: 30,
  geometries: true
});

print('Labeled points:', labeled.size());

var dataset = stacked.sampleRegions({
  collection: labeled,
  scale: 20,
  geometries: false
});

Export.table.toDrive({
  collection: dataset,
  description: 'MCTNet_Arkansas_2021_36t',
  fileFormat: 'CSV'
});

print('Check Tasks tab');