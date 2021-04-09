// Create variable for different base maps

var light = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/light-v10',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: mapboxApiKey});

var streets = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: mapboxApiKey});

// Create specific incident layer and use onEachFeature to show certain info for each feature

var pointObject = L.geoJSON(pointObj, {

    onEachFeature: function (feature, layer) {
        layer.bindPopup(`Incident: ${feature.properties.name}`);
        }
});

// Create all incident layer and use onEachFeature to show certain info for each feature

var allPointObject = L.geoJSON(allPointObj, {

    onEachFeature: function (feature, layer) {
        myUrl = `http://dmapps/en/whalebrary/incident_detail/${feature.properties.pk}/view/`
        layer.bindPopup(`Incident: <a href = "${myUrl}">${feature.properties.name}</a>`);
        }
});

// Create the map starting location and zoom level and tell it which layers to have on by default

var map = L.map('map3', {
    // center: [48.46, -61.95],
    // zoom: 6,
    layers: [streets, pointObject] //this says what to have on by default
});

// Create basemaps variable and add basemaps desired to it as options

var baseMaps = {
    "Light": light,
    "Streets": streets,
};

var overlayMaps = {
    "incident": pointObject,
    "all": allPointObject,

};

// Create the control layer box and add baseMaps and overlayMaps to it

L.control.layers(baseMaps, overlayMaps).addTo(map);
map.fitBounds(pointObject.getBounds());
map.setZoom(6);

// add print buttons from https://github.com/rowanwins/leaflet-easyPrint

L.easyPrint({
	title: 'Save to .png',
	position: 'topleft',
	sizeModes: ['Current', 'A4Portrait', 'A4Landscape'],
    exportOnly: 'true'
}).addTo(map);

L.easyPrint({
	title: 'Print to pdf',
	position: 'topleft',
	sizeModes: ['Current', 'A4Portrait', 'A4Landscape']
}).addTo(map);
