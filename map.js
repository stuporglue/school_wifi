// Global variables
var map;
var layers = {};
var breaks;
var popup = null;
var slider;
var currentFloors = [];
var floorOrder = [ "0A", "0B", "0C", "0F", "0G", "0M", "0P", "OS", "S2", "S1", "SB", "SP", "00", "LL", "01", "MZ", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18" ];

// function called when clicking a building polygon
// Argument layer might actually be a feature. Not sure yet
function showBuilding(e){
    // Clean your room!
    layers.rooms.clearLayers();
    layers.hiddenFloors = {};

    if(typeof slider._map != 'undefined' && slider._map !== null){
        map.removeControl(slider);
    }

    // Restore hidden building poly
    if(layers.hiddenBuilding !== null){
        layers.choro.addLayer(layers.hiddenBuilding);
        layers.hiddenBuilding = null;
    }

    if(popup !== null){
        map.closePopup(popup);
        popup = null;
    }

    // Zoom and pan to building the user has clicked so they can see the rooms better

    // Get the rooms for the selected building
    $.getJSON("./queries/building_by_id.py?building=" + e.target.feature.properties.building_n, function(json){

            //.setLatLng(e.latlng)
        if(json.features.length === 0){
            $.getJSON("./queries/jacks_by_building_id.py?building=" + e.target.feature.properties.building_n, function(wifilist){
                var html = "<p>We don't have a map of the rooms in this building, but we do have this list of Wifi points</p>";
                html += "<p><dl>";
                html += "<dt>ST_Area</dt><dd>" + e.target.feature.properties.buildingarea + "</dd>";
                html += "<dt>shape_area</dt><dd>" + e.target.feature.properties.shape_area + "</dd>";
                html += "<dt>Jacks</dt><dd>" + e.target.feature.properties.jackcount + "</dd>";
                html += "</dl></p>";
                html += "<div class='aptable'><table><tr><th>Floor</th><th>Room(s)</th></tr>";
                for(var i = 0;i<wifilist.length;i++){
                    html += "<tr><td>" + wifilist[i]['floor'] + "</td><td>" + wifilist[i]['rooms'].join(', ') + "</td><tr>";
                }
                html += "<table></div>";

                popup = L.popup()
                .setLatLng(JSON.parse(e.target.feature.properties.centroid).coordinates.reverse())
                .setContent(html)
                .openOn(map);
                return;
            });

            return;
        }

        // Move the clicked building to the hiddenBuilding holding place
        layers.hiddenBuilding = e.target;
        map.fitBounds(layers.hiddenBuilding.getBounds());
        layers.choro.removeLayer(e.target);

        // Move each polygon into an appropriate array in hiddenFloors
        currentFloors = [];
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
            return floorOrder.indexOf(a) - floorOrder.indexOf(b);
        });

        slider.addTo(map);
        replaceSlider(currentFloors.length - 1,0);

        // Add a single floor to the map
        // TODO: Add the ground floor instead of the first sorted floor
        layers.rooms.addData(layers.hiddenFloors[currentFloors[0]]);
    });
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
    $.getJSON("./queries/mactrac.py",function(json){
        layers.choro = L.geoJson(json,{
            onEachFeature: function(feature,layer){
                layer.on('click',showBuilding);
            },
            style: style
        });
        map.addLayer(layers.choro); 
    });

    // Make the Jenks key
    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
        var htmlstr = '';
        htmlstr += "<div id='wifilegend'>";
        htmlstr += "<div id='morewifi'>More Wifi</div>";
        htmlstr += "<div id='lesswifi'>Less Wifi</div>";
        htmlstr += "<div id='nowifi'>No Wifi</div>";
        htmlstr += "</div>";
        div.innerHTML += htmlstr;
        return div;
    };

    legend.addTo(map);

    // Add an empty rooms layer to show rooms on later
    layers.rooms = L.geoJson();
    map.addLayer(layers.rooms);

    // Make objects to store hidden stuff
    // hiddenBuilding holds a single building at a time (the building having the floors shown)
    // hiddenFloors is a hash holding each layer of the building
    layers.hiddenBuilding = null;
    layers.hiddenFloors= {};
	
	slider = L.control({position: 'topright'});

    slider.onAdd = function (map) {
        var div = L.DomUtil.create('div', 'info legend');
            div.innerHTML += '<div id="slider-vertical"></div>';

        var stop = L.DomEvent.stopPropagation;

        L.DomEvent
            .on(div, 'click', stop)
            .on(div, 'mousedown', stop)
            .on(div, 'dblclick', stop);

        return div;
    };

}

mapInit();
