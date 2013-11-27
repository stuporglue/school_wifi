jenksbuckets = ['#ffeda0',
'#ffa700',
'#ffbf00',
'#ffd200',
'#fff200',
'#f6fc00',
'#edfc00',
'#defc00',
'#d0fd00',
'#c2fd00',
'#b6fd00',
'#a7fd00',
'#99fd00',
'#8dfe00',
'#7afe00',
'#70fe00'
             ];

function getColor(bucket) {
    if(typeof bucket != 'number'){
        return jenksbuckets[0];
    }
    return jenksbuckets[bucket];
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
