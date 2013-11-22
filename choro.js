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
