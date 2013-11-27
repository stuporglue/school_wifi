function sliderCallback(event,ui){
    layers.rooms.clearLayers();
    layers.rooms.addData(layers.hiddenFloors[currentFloors[ui.value]]);

    layers.points.clearLayers();
    layers.points.addData(layers.hiddenPoints[currentPoints[ui.value]]);
}

function replaceSlider(floorCount,curFloor){
    $( "#slider-vertical" ).slider({
      orientation: "vertical",
      range: "min",
      min: 0,
      max: floorCount,
      value: curFloor,
	  step: 1,
      slide: sliderCallback
    });
}
