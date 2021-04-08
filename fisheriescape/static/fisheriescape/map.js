// Create some test points and group in a layer

var point1 = L.marker([48.76, -60.87]).bindPopup('Test 1'),
    point2 = L.marker([48.30, -63.68]).bindPopup('Test 2');

var tests = L.layerGroup([point1, point2]);

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

// Create the map starting location and zoom level and tell it which layers to have

var map = L.map('map', {
    center: [48.46, -61.95],
    zoom: 6,
    layers: [light, streets]
});


// Create subfunctions for lobsterFishery polygon layer

function showInfo() {
    this.setStyle({
        'fillColor': '#689ae9'
    });
}

function removeInfoLobster() {
    lobsterFishery.resetStyle(this);
    }

function removeInfoCrab() {
    snowCrabFishery.resetStyle(this);
}

function removeInfoNafo() {
    nafoFishery.resetStyle(this);
}


// Create Lobster polygon layer and use onEachFeature to show certain info for each feature

var lobsterFishery = L.geoJSON(lobsterObj, {
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
            mouseout: removeInfoLobster
        });
        }
});

// Create Snowcrab polygon layer and use onEachFeature to show certain info for each feature

var snowCrabFishery = L.geoJSON(snowCrabObj, {
    style: function() {
        return {
            color: 'yellow'
        }
    },
    onEachFeature: function (feature, layer) {
        myUrl = `http://dmapps/en/fisheriescape/fisheryarea/${feature.properties.pk}/view/`
        layer.bindPopup(`Name: <a href = "${myUrl}">${feature.properties.name}</a></br>Layer ID: ${feature.properties.layer_id}</br>Region: ${feature.properties.region}`);
        layer.on({
            mouseover: showInfo,
            mouseout: removeInfoCrab
        });
        }
});

// Create NAFO polygon layer and use onEachFeature to show certain info for each feature

// var nafoFishery = L.geoJSON(nafoObj, {
//     style: function() {
//         return {
//             color: 'green'
//         }
//     },
//     onEachFeature: function (feature, layer) {
//         myUrl = `http://dmapps/en/fisheriescape/fisheryarea/${feature.properties.pk}/view/`
//         layer.bindPopup(`Name: <a href = "${myUrl}">${feature.properties.name}</a></br>Layer ID: ${feature.properties.layer_id}</br>Region: ${feature.properties.region}`);
//         layer.on({
//             mouseover: showInfo,
//             mouseout: removeInfoNafo
//         });
//         }
// });


// Create basemaps variable and add basemaps desired to it as options

var baseMaps = {
    "Light": light,
    "Streets": streets
};

// Create overlay variable and add overlays desired

var overlayMaps = {
    "Test": tests,
    "Lobster Areas": lobsterFishery,
    "Snow Crab Areas": snowCrabFishery,
    // "NAFO Areas": nafoFishery
};

// Create the control layer box and add baseMaps and overlayMaps to it

L.control.layers(baseMaps, overlayMaps).addTo(map);