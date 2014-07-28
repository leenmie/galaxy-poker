/*
 * This module implements sprite sheet exported from TexturePacker (json format)
 * jquery is required to load json file.
 */

ig.module(
		'plugins.sprite'
).requires(
		'impact.image'
).defines(function() {
"use strict";

ig.SpriteSheet = ig.Class.extend({
	image: null,
	sprites: {},
	frames: [],
	loaded: false,
	staticInstantiate: function(path, json_path) {
		return ig.SpriteSheet.cache[path] || null;
	},
	init: function(path, json_path) {		
		this.image = new ig.Image(path);
		var _this = this;
		$.getJSON(json_path, function(data){
			_this.load_json(data);
		});
		ig.SpriteSheet.cache[path] = this;		
	},
	load_json: function(data) {
		console.log(data);
		var frames = data.frames;
		this.frames = frames;
		var i = 0;
		for (i=0; i<frames.length; i++) {
			var frame = frames[i];
			this.sprites[frame.filename] = frame.frame;
		}
		this.loaded = true;
	}
});

ig.SpriteSheet.cache = {};

ig.Sprite = ig.Class.extend({
	
	sprite_sheet: null,
	sprite_name: null,
	init: function(sprite_sheet, sprite_name) {
		this.sprite_sheet = sprite_sheet;
		this.sprite_name = sprite_name;
	},
	draw: function(targetX, targetY) {
		if (this.sprite_sheet.loaded && this.sprite_sheet.image) {
			var sourceX = this.sprite_sheet.sprites[this.sprite_name].x;
			var sourceY = this.sprite_sheet.sprites[this.sprite_name].y;
			var width = this.sprite_sheet.sprites[this.sprite_name].w;
			var height = this.sprite_sheet.sprites[this.sprite_name].h;
			this.sprite_sheet.image.draw(targetX, targetY, sourceX, sourceY, width, height);
		}
	}
});

});