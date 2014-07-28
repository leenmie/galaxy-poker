ig.module( 
	'game.entities' 
)
.requires(
	'impact.entity',
	'impact.animation',
	'plugins.newentity',
	'plugins.utils',
	'plugins.sprite'
)
.defines(function(){

SoldierEntity = ig.Entity.extend({
    name: "soldier",
	back: false,
	moving: 0,
	original_y: 0,
	moveForward: function(distance) {
		this.moving = distance;
		this.original_y = this.pos.y;
		if (!this.back) {
			this.vel.y += 50;
		}
		else {
			this.vel.y -= 50;
		}
	},
	turn_back: function() {
		this.back = true;
	},
	update:function() {
		if (this.moving) {
			if (Math.abs(this.pos.y - this.original_y)>= this.moving) {
				this.vel.y = 0;
				this.pos.y = this.original_y + 
							(this.pos.y - this.original_y)/Math.abs(this.pos.y - this.original_y)*this.moving;
				this.moving = 0;
			}
		}
		this.parent();
	}
});

GreenSoldierEntity = SoldierEntity.extend({
    size: {x:21, y:24},
    animSheet: new ig.AnimationSheet('media/graphics/game/green_soldier.png', 21, 24),
    
    init: function(x, y, settings) {
		var speed = getRandomArbitary(0.2, 0.4);
        this.addAnim('walk', speed, [0, 1, 2, 3]);        
        this.parent(x, y, settings);
        if (ig.system.width > 640) {
			this.setScale(2, 2);
		}
    },
    turn_face: function() {
		this.currentAnim = this.anims.walk;
	},
    turn_back: function() {
		this.parent();
		var speed = getRandomArbitary(0.2, 0.4);
		var ani_sheet = new ig.AnimationSheet('media/graphics/game/green_soldier_back.png', 27, 23);
		var ani = new ig.Animation(ani_sheet, speed, [0, 1, 2]);
		this.currentAnim = ani;
	}
                
});

MechEntity = SoldierEntity.extend({
    size: {x: 38, y: 36},
    animSheet: new ig.AnimationSheet('media/graphics/game/mech.png', 38, 36),
    
    init: function(x, y, settings) {
		var speed = getRandomArbitary(0.2, 0.4);
        this.addAnim('walk', speed, [0, 1]);        
        this.parent(x, y, settings);
    },
    turn_face: function() {
		this.parent();
		this.currentAnim = this.anims.walk;
	},
    turn_back: function() {
		this.parent();
		var speed = getRandomArbitary(0.2, 0.4);
		var ani_sheet = new ig.AnimationSheet('media/graphics/game/mech_back.png', 41, 35);
		var ani = new ig.Animation(ani_sheet, speed, [0, 1]);
		this.currentAnim = ani;
	}
                
});

HealthBarEntity = ig.Entity.extend({
    name: "bar",
    size: {x: 100, y: 22},
    animSheet: new ig.AnimationSheet('media/graphics/interface/health_bar.png', 100, 22),
    
    init: function(x, y, settings) {
        this.addAnim('idle', 1, [0]);
        this.parent(x, y, settings);
    }
});

HealthValueEntity = ig.Entity.extend({
    name: "bar",
    size: {x: 76, y: 14},
    font: new ig.Font('media/freemono.font.png'),
    animSheet: new ig.AnimationSheet('media/graphics/interface/health_value.png', 76, 14),
    zIndex: 999,
    init: function(x, y, settings) {
        this.addAnim('idle', 0.2, [0]);
        this.parent(x, y, settings);
    },
    max_hp : 100,
    current_hp : 100,    
    percent: 1,
    visible: true,
    setHP: function(hp) {
        this.current_hp = hp;
    },
    draw: function() {        
		if (this.visible) {
			var percent = (this.current_hp / this.max_hp).round(1);
			this.percent = percent;
			percent = (percent > 1 ? 1 : percent);
			if (percent <= 1) {									
    			if (this.scale.x > percent) {
    				this.scale.x -= 0.01;            
    			}			
    			if (this.scale.x < percent) {				
    				this.scale.x += 0.01;            
    			}
    			if (this.scale.x <= 0.01) {
    				this.visible = false;					
    			}
			}
			this.parent();
		}
		this.font.draw(String(this.current_hp), this.pos.x + this.size.x / 3, this.pos.y - 1);
    },
    reset: function() {
		this.visible = true;
		this.scale.x = 1;
		this.current_hp = this.max_hp;
		var _x = this.pos.x;
		var _y = this.pos.y;
		this.parent();
		this.pos.x = _x;
		this.pos.y = _y;
	}
    
});

CARD_WIDTH = 90;
CARD_HEIGHT = 128;

CardUpEntity = ig.Entity.extend({
    name: "card",
    size: {x: CARD_WIDTH, y:CARD_HEIGHT},
    //animSheet: new ig.AnimationSheet('media/graphics/game/card_deck_small.png', 50, 70),
    value: 0,
    zIndex: 999,
    highlight: false,
    sprite_sheet: null,
    current_sprite: null,
    init: function(x, y, settings) {
    	this.parent(x, y, settings);
        /*for (var i=0; i<52; i++) {
            var suit = (i / 13).toInt();
            var number = i % 13;
            var card_value = 'card' + (number * 4 + suit);
            this.addAnim(card_value, 1, [i]);
        }
        this.parent(x, y, settings);
        var scale_x = this.size.x / 50;
        var scale_y = this.size.y / 70;
        this.setScale(scale_x, scale_y);*/
    	var sprite_sheet = new ig.SpriteSheet('media/graphics/game/cards.png', 'media/graphics/game/cards.json');
    	this.sprite_sheet = sprite_sheet;
    },
    
    setCardValue: function(value) {
    	if (value < 0 || value > 51) {
    		return;
    	}
    	this.value = value;
        /*this.currentAnim = this.anims['card'+value];*/
    	var sprite = new ig.Sprite(this.sprite_sheet, String(value)+'.png');
    	this.current_sprite = sprite;
    },
    
    draw: function() {
        this.parent();
        if (this.current_sprite) {
        	this.current_sprite.draw(this.pos.x, this.pos.y);
        }
        if (this.highlight) {
            var ctx = ig.system.context;
            ctx.beginPath();
            ctx.lineWidth="4";
            ctx.strokeStyle="red";
            ctx.rect(this.pos.x+2, this.pos.y+2, this.size.x-4, this.size.y-4); 
            ctx.stroke();        
        }        
    }    
});

CardDownEntity = ig.Entity.extend({
    name: "card",
	size: {x: CARD_WIDTH, y: CARD_HEIGHT},
	animSheet: new ig.AnimationSheet('media/graphics/game/card_down.png', 90, 128),
	zIndex: 998,
    init: function(x, y, settings) {
        this.parent(x, y, settings);
        this.addAnim('card', 1, [0]);              
    },
});

ExplosionEntity = ig.Entity.extend({
	size: {x: 42, y: 42},
	animSheet: new ig.AnimationSheet('media/graphics/game/explosion.png', 42, 42),
    init: function(x, y, settings) {
        this.parent(x, y, settings);
        var speed = getRandomArbitary(0.2, 0.4);
        this.addAnim('explosion', speed, [0, 1, 2, 3, 4, 5, 6, 7, 8], true);       
    },
    update: function() {
		this.parent();
		if (this.currentAnim.frame == 8) {
			var _this = this;
			setTimeout(
				function(){
					_this.kill();
				},
				200);
		}
	}
});

ShipEntity = ig.Entity.extend({
	zIndex: 9999,
	rotate: function(rad) {
		this.currentAnim.angle = rad;
	},
	moveTo: function(to_x, to_y, duration) {		
		var rad = calculate_angle(this.pos.x, this.pos.y, to_x, to_y);		
		this.rotate(rad);
		this.parent(to_x, to_y, duration);
	},
	killLater: function(milisecond) {
		var _this = this;
		setTimeout(
			function() {
				_this.kill();
			},
			milisecond
		);
	}
});

BattleShipEntity = ShipEntity.extend({
	size: {x: 127, y: 106},
	animSheet: new ig.AnimationSheet('media/graphics/game/battleship.png', 127, 106),
    init: function(x, y, settings) {
        this.parent(x, y, settings);
        this.addAnim('fly', 1, [0], true);       
    },	
});

SmallShipEntity = ShipEntity.extend({
	size: {x: 82, y: 74},
	animSheet: new ig.AnimationSheet('media/graphics/game/smallship.png', 82, 74),
    init: function(x, y, settings) {
        this.parent(x, y, settings);
        this.addAnim('fly', 1, [0], true);       
    },
});

BigBlindEntity = ig.Entity.extend({
    name: "button",
    zIndex: 5,
    size: {x: 30, y:30},
    animSheet: new ig.AnimationSheet('media/graphics/interface/big_blind_button.png', 30, 30),
    init: function(x, y, settings) {
        this.parent(x, y, settings);
        this.addAnim('fly', 1, [0], true);       
    },
});

SmallBlindEntity = ig.Entity.extend({
    name: "button",
    zIndex: 5,
    size: {x: 30, y: 30},
    animSheet: new ig.AnimationSheet('media/graphics/interface/small_blind_button.png', 30, 30),
    init: function(x, y, settings) {
        this.parent(x, y, settings);
        this.addAnim('fly', 1, [0], true);       
    },
});

TimeBarEntity = ig.Entity.extend({
    name: "bar",
    size: {x: 100, y: 15},
    animSheet: new ig.AnimationSheet('media/graphics/interface/time_bar.png', 100, 15),
    init: function(x, y, settings) {
        this.parent(x, y, settings);
        this.addAnim('fly', 1, [0], true);       
    },
});

PotEntity = ig.Entity.extend({
    name: "pot",
    zIndex: 4,
    size: {x: 60, y: 30},
    font: new ig.Font('media/ubuntu.font.png'),
    value: 0,
    animSheet: new ig.AnimationSheet('media/graphics/interface/pot.png', 60, 30),
    init: function(x, y, settings) {
        this.parent(x, y, settings);
        this.addAnim('fly', 1, [0], true);       
    },
    draw: function() {
        this.parent();
        this.font.draw(String(this.value), this.pos.x + 10, this.pos.y + 4);
    }
     
});

DialogEntity = ig.Entity.extend({
    name: "dialog",
    zIndex: 10000,
    size: {x: 300, y:141},
    font: new ig.Font('media/freemono.font.png'),
    text: "Text",
    animSheet: new ig.AnimationSheet('media/graphics/interface/dialog.png', 300, 141),
    init: function(x, y, settings) {
        this.parent(x, y, settings);
        this.addAnim('dialog', 1, [0], true);       
    },
    draw: function() {
        this.parent();
        this.font.draw(this.text, this.pos.x + this.size.x/2, this.pos.y + 20, ig.Font.ALIGN.CENTER);
    }
});

BackgroundEntity = ig.Entity.extend({
	name: "background",
	zIndex: -10000,
	size: {x: 1024, y: 1024},
	speed: 100,//20 pixel per second
	save_pos: {x: 0, y:0},
	animSheet: new ig.AnimationSheet('media/graphics/game/galaxy2.png', 1024, 1024),
	head: null,
	tail: null,
	init: function(x, y, settings) {
		this.parent(x, y, settings);
		this.addAnim('galaxy', 1, [0], true);
		this.moveTop();
	},
	moveTop: function() {
		this.save_pos.y = this.pos.y;
		this.moveTo(this.pos.x, this.pos.y - this.size.y, this.size.y/this.speed);
	},
	stopMoving: function(x, y) {
		this.parent(x, y);
		if (this.pos.y <= this.save_pos.y - this.size.y) {
			if (this.pos.y < -100) {
				this.pos.y = this.size.y - 5;
			}
			this.moveTop();
		}
	},
	update: function() {
		this.parent();				
	}	
});

BackgroundRotateEntity = ig.Entity.extend({
	size: {x: 1024, y: 1024},
	animSheet: new ig.AnimationSheet('media/graphics/game/galaxy2.png', 1024, 1024),
	init: function(x, y, settings) {
		this.parent(x, y, settings);
		this.addAnim('galaxy', 1, [0], true);		
	},
	update: function() {
		this.parent();
		this.currentAnim.angle -= 0.0005;
	}
	
});

BulletEntity = ig.Entity.extend({
	size: {x: 16, y: 11},
	animSheet: new ig.AnimationSheet('media/graphics/game/bullets.png', 16, 11),
	init: function(x, y, settings) {
		this.parent(x, y, settings);
		var index = getRandomInt(0, 5);
		this.addAnim('bullet', 1, [index], true);
	},
	moveTo: function(to_x, to_y, duration) {
		this.parent(to_x, to_y, duration);
		this.currentAnim.angle = calculate_angle(this.pos.x, this.pos.y, to_x, to_y);
	},
	stopMoving: function(x, y) {
		this.parent(x, y);
		this.kill();
	}
});

});
