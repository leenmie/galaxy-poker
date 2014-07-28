ig.module( 
	'plugins.utils' 
)
.defines(function(){

getRandomInt = function (min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};

getRandomArbitary = function (min, max) {
    return Math.random() * (max - min) + min;
};

calculate_angle = function(from_x, from_y, to_x, to_y) {
	var dx = to_x - from_x;
	var dy = to_y - from_y;	
	var rad = 0;
	rad = Math.atan(dy/dx);
	if (dx < 0 && dy < 0) {
		rad = rad + Math.PI;
	}
	if (dx < 0 && dy >= 0) {
		rad = rad - Math.PI;
	}
	if (dx > 0 && dy < 0) {
		rad = 2*Math.PI + rad;
	}
	/*if (dx == 0) {				
		if (dy < 0) {
			rad = -Math.PI/2;
		}
	}*/
	
	/*if (dx == 0) {
		if (dx >= 0) {
			rad = 0;
		}
		else {
			rad = Math.PI;
		}
	}
	else {
		rad = Math.atan(dy/dx);
		if (dx < 0 && dy < 0) {
			rad = rad + Math.PI;
		}
		if (dx <= 0 && dy > 0) {
			rad = rad + Math.PI/2;
		}
		if (dx == 0) {				
			if (dy < 0) {
				rad = -Math.PI/2;
			}
		}				
	}*/
	return rad;
	
};

});
