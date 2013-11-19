// Global variables
var map;
var layers = {};
var breaks;

// function called when clicking a building polygon
// Argument layer might actually be a feature. Not sure yet
function showBuilding(e){
    // Clean your room!
    layers.rooms.clearLayers();
    layers.hiddenFloors = {};

    // Restore hidden building poly
    if(layers.hiddenBuilding !== null){
        layers.choro.addLayer(layers.hiddenBuilding);
    }

    // Move the clicked building to the hiddenBuilding holding place
    layers.hiddenBuilding = e.target;
    layers.choro.removeLayer(e.target);

    // Zoom and pan to building the user has clicked so they can see the rooms better
    map.fitBounds(layers.hiddenBuilding.getBounds());

    // Get the rooms for the selected building
    $.getJSON("./queries/building_by_id.py?building=" + layers.hiddenBuilding.feature.properties.building_n, function(json){

        // Move each polygon into an appropriate array in hiddenFloors
        var currentFloors = [];
        for(var i = 0;i<json.features.length;i++){
            if(typeof layers.hiddenFloors[json.features[i].properties.floor] == 'undefined'){
                layers.hiddenFloors[json.features[i].properties.floor] = [];
                currentFloors.push(json.features[i].properties.floor);
            }
            layers.hiddenFloors[json.features[i].properties.floor].push(json.features[i]);
        }

        // Sort the floor numbers in order of lowest to highest
        // TODO: Replace this with a sort function that actually sorts floors with the letters in them
        currentFloors.sort(function(a,b){
            return a - b;
        });

        // Add a single floor to the map
        // TODO: Add the ground floor instead of the first sorted floor
        layers.rooms.addData(layers.hiddenFloors[currentFloors[0]]);
    });
}

function getColor(bucket) {
    return bucket == 5 ? '#800026' :
           bucket == 4  ? '#BD0026' :
           bucket == 3  ? '#E31A1C' :
           bucket == 2  ? '#FC4E2A' :
           bucket == 1   ? '#FD8D3C' :
                      '#FFEDA0';
}

function style(feature) {
    return {
        fillColor: getColor(feature.properties.jenks),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function mapInit(){
    // Make the map object
    map = L.map('map').setView([44.9722898,-93.23534488], 16);


    // Add the basemap to the map
    layers.tiles = L.tileLayer('http://{s}.tiles.mapbox.com/v3/stuporglue.g8224njj/{z}/{x}/{y}.png', {
        attribution: "<a href='https://www.mapbox.com'>MapBox</a>",
        maxZoom: 22
    });
    map.addLayer(layers.tiles);


    // Add buildings to the map
    //$.getJSON("./queries/buildings.py",function(json){
    //    layers.buildings = L.geoJson(json,{
    //        onEachFeature: function(feature,layer){
    //            layer.on('click',showBuilding);
    //        }
    //    });
    //    // map.addLayer(layers.buildings); 
    //});

    // Add buildings to the map
    $.getJSON("./queries/mactrac.py",function(json){
        layers.choro = L.geoJson(json,{
            onEachFeature: function(feature,layer){
                layer.on('click',showBuilding);
            },
            style: style
        });
        map.addLayer(layers.choro); 
    });

    // Get breaks for key
    $.getJSON("./queries/breaks.py",function(json){
        breaks = json;
    });


    // Add an empty rooms layer to show rooms on later
    layers.rooms = L.geoJson();
    map.addLayer(layers.rooms);

    // Make objects to store hidden stuff
    // hiddenBuilding holds a single building at a time (the building having the floors shown)
    // hiddenFloors is a hash holding each layer of the building
    layers.hiddenBuilding = null;
    layers.hiddenFloors= {};
}

mapInit();
