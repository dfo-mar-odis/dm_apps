
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


// Create subfunctions for polygon layer

function showInfo() {
    this.setStyle({
        'fillColor': '#689ae9'
    });
}

function removeInfoPolygon() {
    polygonObject.resetStyle(this);
    }

// Create polygon layer and use onEachFeature to show certain info for each feature

var polygonObject = L.geoJSON(polygonObj, {
    style: function() {
        return {
            color: 'blue'
        }
    },
    onEachFeature: function (feature, layer) {
        myUrl = `http://dmapps/en/fisheriescape/fisheryarea/${feature.properties.pk}/view/`
        layer.bindPopup(`Name: <a href = "${myUrl}">${feature.properties.name}</a></br>Layer ID: ${feature.properties.layer_id}</br>Region: ${feature.properties.region}`);
        layer.on({
            mouseover: showInfo,
            mouseout: removeInfoPolygon
        });
        }
});


// Create the map starting location and zoom level and tell it which layers to have on by default

var map = L.map('map2', {
    // center: [48.46, -61.95],
    // zoom: 6,
    layers: [streets, polygonObject] //this says what to have on by default
});

// Create basemaps variable and add basemaps desired to it as options

var baseMaps = {
    "Light": light,
    "Streets": streets,
};

var overlayMaps = {
    "Fishery": polygonObject,

};

// Create the control layer box and add baseMaps and overlayMaps to it

L.control.layers(baseMaps, overlayMaps).addTo(map);
map.fitBounds(polygonObject.getBounds(), {padding: [50, 50]});