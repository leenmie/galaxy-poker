ig.module( 
	'game.play' 
)
.requires(
	'impact.game',
	'impact.font',
	'impact.input',
	'impact.background-map',
	'game.entities',
	'plugins.utils',
	'plugins.touch-button'
)
.defines(function(){

TURN_WAITING_TIME = 30;

PokerGame = ig.Game.extend({
	name: "PlayingScene",
	buttons: null,
	up_army: [],
	down_army: [],
	up_hand: [],
	down_hand: [],
	dealing_cards: [],
	up_health_bar: null,
	down_health_bar: null,
	default_stake: 100,
	time_last_deal: 0,
	big_blind: null,
	small_blind: null, 
	time_bar:null,
	timer: new ig.Timer(),
	waiting: false,
	confirm_dialog: null,
	down_pot: null,
	up_pot: null,
	positions: null,
	//card_zIndex: 999,
	sounds: {
		call: new ig.Sound('media/sounds/coin.ogg'),
		check: new ig.Sound('media/sounds/knock.ogg'),
		deal: new ig.Sound('media/sounds/liftoff.ogg'),
		showdown: new ig.Sound('media/sounds/reveal.ogg'),
		win: new ig.Sound('media/sounds/win.ogg'),
		lose: new ig.Sound('media/sounds/penalty.ogg'),
		click: new ig.Sound('media/sounds/ready.ogg')
	},
	init: function() {
	    if (GAME) {
	       GAME.game = this;
	    }
		this.time_last_deal = ig.system.clock.last;
		this.waiting_text = new ig.Font('media/a.font.png');
		this.drawWaitingScene();
		this.init_positions();
		this.init_input();
		//this.startGame();		
		// On game start				
		//this.drawPreFlop();
		//this.drawFlop();
		//this.drawTurn();
		//this.drawRiver();
	},
	
	init_positions: function() {
		this.positions = {
			up_pot: {x: ig.system.width - 100, y: 60},
			down_pot: {x: ig.system.width - 100, y: ig.system.height - 100},
			up_blind: {x: ig.system.width - 40, y: 60},
			down_blind: {x: ig.system.width - 40, y: ig.system.height - 100},
			enemy_cards: {x: 240, y:40},
			player_cards: {x: 240, y: ig.system.height - 150},
			flop_cards: {x: 100, y: (ig.system.height - 130)/2},
			turn_card: {x: 370, y: (ig.system.height - 130)/2},
			river_card: {x: 460, y: (ig.system.height - 130)/2}			
		};
	},
	
	init_input: function() {
		ig.input.bind( ig.KEY.LEFT_ARROW, 'call' );
		ig.input.bind( ig.KEY.RIGHT_ARROW, 'raise' );
		ig.input.bind( ig.KEY.UP_ARROW, 'fold' );		
		ig.input.bind( ig.KEY.ESC, 'exit');
		ig.input.bind( ig.KEY.SPACE, 'ready');
		var image_button_call = new ig.Image('media/graphics/interface/button_call.png');
		var image_button_raise = new ig.Image('media/graphics/interface/button_raise.png');
		var image_button_fold = new ig.Image('media/graphics/interface/button_fold.png');
		var image_button_exit = new ig.Image('media/graphics/interface/button_exit.png');
		this.buttons = new ig.TouchButtonCollection([
			new ig.TouchButton( 'call', {left: 0, bottom: 0}, 35, 35, image_button_call, 0 ),
			new ig.TouchButton( 'raise', {left: 35, bottom: 0}, 35, 35, image_button_raise, 0 ),
			new ig.TouchButton( 'fold', {left: 70, bottom: 0}, 35, 35, image_button_fold, 0 )			
		]);
		this.buttons.align();
		this.exit_button = new ig.TouchButtonCollection([
		  new ig.TouchButton( 'exit', {left: 0, top: 0}, 35, 35, image_button_exit, 0 )
		]);	
		this.exit_button.align();
		
		this.confirm_button = new ig.TouchButtonCollection([
            new ig.TouchButton( 'ready', 
                                {left: (ig.system.width - 35) /2, top: (ig.system.height - 35)/2}, 
                                35, 
                                35, 
                                image_button_call, 
                                0),
        ]);
        this.confirm_button.align();
	},
	
	drawBigBlind: function(side) {
	   if (side == "up") {
	       this.big_blind = this.spawnEntity(BigBlindEntity, this.positions.up_blind.x, this.positions.up_blind.y); 
	       this.small_blind = this.spawnEntity(SmallBlindEntity, this.positions.down_blind.x, this.positions.down_blind.y);       
	   }
	   else if (side == "down") {
	       this.big_blind = this.spawnEntity(BigBlindEntity, this.positions.down_blind.x, this.positions.down_blind.y);
	       this.small_blind = this.spawnEntity(SmallBlindEntity, this.positions.up_blind.x, this.positions.up_blind.y); 
	   } 	       
	},
	
	drawPots: function() {
	   if (!this.up_pot) {
	       this.up_pot = this.spawnEntity(PotEntity, this.positions.up_pot.x, this.positions.up_pot.y);
	   }
	   if (!this.down_pot) {
	       this.down_pot = this.spawnEntity(PotEntity, this.positions.down_pot.x, this.positions.down_pot.y);
	   }
	},
	
	drawWaitingScene: function() {
	    this.drawBackgroundMap();
		this.drawGalaxyMap();
	    this.waiting = true;
	},
	
	drawTimeBar: function(side) {
	    var x = ig.system.width - 100;
	    var y = this.down_health_bar.pos.y - 20;
	    if (side == "up") {	        
	        y = this.up_health_bar.pos.y + 20;
	    }
	    if (this.time_bar) {
	        this.time_bar.kill();
	    }
	    this.time_bar = this.spawnEntity(TimeBarEntity, x, y);
	    this.timer.set(TURN_WAITING_TIME);
	},
	
	startGame: function() {
	    this.waiting = false;	
	    //this.card_zIndex = 999;
		this.drawBombing();	
		var _this = this;
		setTimeout(
			function() {
				_this.drawArmy();
				_this.drawHealthBar();
				_this.drawPots();					
				_this.sortEntities();
				GAME.pause_processing = false;
			},
			1500
		);
		this.closeConfirmDialog();
	},
		
	clearGame: function() {
        //delete army
        for (var i=0; i<this.entities.length; i++) {
            var name = this.entities[i].name;
            if (name == "soldier" || name == "bar" || name == "card"
                || name == "pot" || name == "button") {
                this.entities[i].kill();
            } 
        }
        this.up_pot = null;
        this.down_pot = null;
        this.waiting = true;
	},
	
	clearCards: function() {
	   for (var i=0; i < this.entities.length; i++) {
	       var name = this.entities[i].name;
	       if (name == "card") {
	           this.entities[i].kill();
	       }
	   }    
	},
	
	highlightCards: function(cards) {
	   for (var i=0; i < this.entities.length; i++) {
           var name = this.entities[i].name;
           if (name == "card") {
               for (var j=0; j < cards.length; j++) {
                   if (this.entities[i].value == cards[j]) {
                       this.entities[i].highlight = true;
                   }
               }
           }
       }
	},
	
	setHP: function(side, hp) {
	    var health_bar = null;
	    if (side == "up") {
	       health_bar = this.up_health_bar;
	    }
	    else if (side == "down") {
	       health_bar = this.down_health_bar;
	    }
	    if (health_bar) {
	       var current_hp = health_bar.current_hp;
	       var diff = current_hp - hp;
	       if (diff > 0) {
	    	   if (hp < health_bar.max_hp) {
	    		   this.takeDamage(side, diff);
	    	   }
	       }
	       else if (diff < 0) {
	    	   if (current_hp < health_bar.max_hp) {
	    		   this.takeReinforcement(side, Math.abs(health_bar.max_hp - current_hp));
	    	   }
	       }
	       health_bar.current_hp = hp;
	    }
	},
	
	drawBombing: function() {
		var x = -80;
		var y = 0;
		var to_x = ig.system.width;
		var to_y = ig.system.height;
		for (var i = 0; i < 10; i++) {
			var r = Math.random();
			if (r<0.5) {
				x = getRandomInt(ig.system.width, ig.system.width + 100);
				to_x = -200;
			}
			else {
				x = getRandomInt(-180, -80);
				to_x = ig.system.width+100;
			}
			y = getRandomInt(0, ig.system.height);
			to_y = getRandomInt(0, ig.system.height);
			r = Math.random();
			var ship_class = BattleShipEntity;
			if (r<0.5) {
				ship_class = SmallShipEntity;
			}
			var ship = this.spawnEntity(ship_class, x, y);
			var speed = getRandomInt(2, 5);
			ship.moveTo(to_x, to_y, speed);	
			ship.killLater(speed*1000);				
		}
		var _this = this;
		setTimeout(
			function() {
				_this.drawBombingExplosion();
			},
			1000
		);
		this.sortEntities(); 
	},	
	
	drawBombingExplosion: function() {
		for (var i = 0; i < 50; i++) {
			var x = getRandomInt(0, ig.system.width);
			var y = getRandomInt(0, ig.system.height);
			this.spawnEntity(ExplosionEntity, x, y);
		}
		this.sortEntities();
	},
	
	drawBackgroundMap: function() {
		var n_column = (ig.system.width / 32).toInt()+1;
		var n_row = (ig.system.height / 32).toInt()+1; 
		var data = [];
		for (var i = 0; i < n_row; i++) {
			var row = [];
			for (var j=0; j < n_column; j++) {
				var r = getRandomInt(1,12);
				row.push(r);
			}
			data.push(row);
		}
		var tile_file = 'media/graphics/game/tile_terrain.png';
		var r = getRandomInt(0, 1);
		if (r == 1) {
			tile_file = 'media/graphics/game/tile_terrain2.png';
		}
		var bg = new ig.BackgroundMap(32, data, tile_file);
		this.backgroundMaps.push(bg);		
	},
	
	drawGalaxyMap: function() {
		//this.spawnEntity(BackgroundNextEntity, (ig.system.width - 1024)/2, (ig.system.height - 1024)/2);
		var up = this.spawnEntity(BackgroundEntity, 0, 0);
		var down = this.spawnEntity(BackgroundEntity, 0, up.size.y-5);
		down.currentAnim.flip.y = true;		
		//down.head = up;
	},
	
	drawArmy: function() {
		var left = 200;
		for (var i = 0; i< 10; i++) {
			var distance = 20;
			var soldier_class = GreenSoldierEntity;
			var r = Math.random();
			if (r < 0.3) {
				soldier_class = MechEntity;
				distance = 35;
			}
			var soldier = this.spawnEntity(soldier_class, left, -30);
			this.up_army.push(soldier);
			soldier.moveForward(50);
			left += distance;
		}
		left = 200;
		for (var i = 0; i< 10; i++) {
			var distance = 20;
			var soldier_class = GreenSoldierEntity;
			var r = Math.random();
			if (r < 0.3) {
				soldier_class = MechEntity;
				distance = 35;
			}
			var soldier = this.spawnEntity(soldier_class, left, ig.system.height);
			soldier.turn_back();
			this.down_army.push(soldier);
			soldier.moveForward(50);
			left += distance;
		}
	},
	
	drawHealthBar: function() {
		var health_bar = new HealthBarEntity();
		var x = ig.system.width - health_bar.size.x;
		var y = ig.system.height - health_bar.size.y;
		health_bar.pos.x = x;
		health_bar.pos.y = y;
		this.entities.push(health_bar);		
		var down_health_bar = this.spawnEntity(HealthValueEntity, x+20, y+5);
		//down_health_bar.current_hp = GAME.my_stake;
		down_health_bar.max_hp = this.default_stake;
		down_health_bar.current_hp = this.default_stake;
		this.down_health_bar = down_health_bar;
		
		var health_bar2 = new HealthBarEntity();
		x = ig.system.width - health_bar2.size.x;
		y = 0;
		health_bar2.pos.x = x;
		health_bar2.pos.y = y;
		this.entities.push(health_bar2);		
		var up_health_bar = this.spawnEntity(HealthValueEntity, x+20, y+5);
		up_health_bar.max_hp = this.default_stake;
        up_health_bar.current_hp = this.default_stake;	
		//up_health_bar.current_hp = GAME.my_stake;	
		this.up_health_bar = up_health_bar;
	},
	
	drawPreFlop: function(cards) {
		var card1 = {
			value: -1,
			position: {
				x: this.positions.enemy_cards.x,
				y: this.positions.enemy_cards.y
			}
		};
		var card2 = {
			value: -1,
			position: {
				x: this.positions.enemy_cards.x + 90,
				y: this.positions.enemy_cards.y
			}
		};
        var card3 = {
            value: cards[0],
            position: {
                x: this.positions.player_cards.x,
                y: this.positions.player_cards.y
            }
        };
		var card4 = {
			value: cards[1],
			position: {
				x: this.positions.player_cards.x + 90,
				y: this.positions.player_cards.y
			}
		};
		if (this.big_blind.pos.y == this.positions.down_blind.y) {
		    this.dealing_cards.push(card3);
		    this.dealing_cards.push(card1);
		    this.dealing_cards.push(card4);
		    this.dealing_cards.push(card2);
		}
		else {		    
            this.dealing_cards.push(card1);
            this.dealing_cards.push(card3);
            this.dealing_cards.push(card2);
            this.dealing_cards.push(card4);            
		}
	},
	
	drawFlop: function(cards) {
		var y = this.positions.flop_cards.y;
		var x = this.positions.flop_cards.x;
		for (var i = 0; i<3; i++) {
			var card1 = {
				value: cards[i],
				position: {
					x: x,
					y: y
				}
			};			
			this.dealing_cards.push(card1);
			x+=90;
		}
	},
	
	drawTurn: function(card) {
		var y = this.positions.turn_card.y;
		var x = this.positions.turn_card.x;
		var card1 = {
			value: card,
			position: {
				x: x,
				y: y
			}
		};			
		this.dealing_cards.push(card1);		
	},
	
	drawRiver: function(card) {
		var y = this.positions.river_card.y;
		var x = this.positions.river_card.x;
		var card1 = {
			value: card,
			position: {
				x: x,
				y: y
			}
		};			
		this.dealing_cards.push(card1);				
	},
	
	drawShowDown: function(cards) {
	   var card1 = {
            value: cards[0],
            position: {
                x: this.positions.enemy_cards.x,
                y: this.positions.enemy_cards.y
            }
        };
        var card2 = {
            value: cards[1],
            position: {
                x: this.positions.enemy_cards.x + 90,
                y: this.positions.enemy_cards.y
            }
        };
        for (var i = 0; i < this.up_hand.length; i++) {
            this.up_hand[i].kill();
        }
        var card = this.spawnEntity(CardUpEntity, card1["position"].x, card1["position"].y);
        card.setCardValue(card1.value);
        //card.zIndex = this.card_zIndex--;
        card = this.spawnEntity(CardUpEntity, card2["position"].x, card2["position"].y);
        card.setCardValue(card2.value);
        //card.zIndex = this.card_zIndex--;
        //this.sortEntities(); 
        this.sounds.showdown.play();
	},
	
	dealCards: function() {
		if (this.dealing_cards.length == 0) {
			return;
		}		
		var last_time = ig.system.clock.last;
		if (last_time - this.time_last_deal > 0.5) {
			var card = this.dealing_cards.shift();
			this.sounds.deal.play();
			if (card["value"] == -1) {
				var card_down = this.spawnEntity(CardDownEntity, 0, 0);
				card_down.moveTo(card["position"].x, card["position"].y, 0.5);
				this.up_hand.push(card_down);
			}
			else {
				var card_up = this.spawnEntity(CardUpEntity, 0, 0);
				card_up.setCardValue(card["value"]);
				card_up.moveTo(card["position"].x, card["position"].y, 0.5);
				//card_up.zIndex = this.card_zIndex--;
			}
			this.time_last_deal = last_time;
		}
	},
	
	drawExplosion: function(side, quantity) {
		var y = 20;
		if (side == "down") {
			y = 430;
		}
		var _this = this;
		for (var i = 0; i < quantity; i++) {			
			var random_time = getRandomInt(200, 500);			
			setTimeout(
				function() {					
					var x = getRandomInt(180, 430);
					var _y = getRandomInt(y, y+20);
					if (side == "down") {
						_y = getRandomInt(y-20, y);
					}
					_this.spawnEntity(ExplosionEntity, x, _y);
				},
				random_time
			);			
		}
	},
	
	drawBullets: function() {
		var i = 0;
		for (i = 0; i<this.up_army.length; i++) {
			var soldier = this.up_army[i];
			if (!soldier._killed) {
				var bullet = this.spawnEntity(BulletEntity, soldier.pos.x, soldier.pos.y);
				var target_x = getRandomInt(150, ig.system.width - 100);
				var target_y = ig.system.height;
				bullet.moveTo(target_x, target_y, 0.5);
			}
		}
		
		for (i = 0; i<this.down_army.length; i++) {
			var soldier = this.down_army[i];
			if (!soldier._killed) {
				var bullet = this.spawnEntity(BulletEntity, soldier.pos.x, soldier.pos.y);
				var target_x = getRandomInt(150, ig.system.width - 100);
				var target_y = -10;
				bullet.moveTo(target_x, target_y, 0.5);
			}
		}
	},
	
	dieSoldier: function(side, quantity) {
		var soldiers = this.up_army;
		if (side == "down") {
			soldiers = this.down_army;
		}
		var i = 0;
		var alive_soldiers = [];
		for (i =0; i < soldiers.length; i++) {
		    if (!soldiers[i]._killed) {
		        alive_soldiers.push(soldiers[i]);
		    }
		}
		for (i = 0; i < quantity; i++) {
			var _index = getRandomInt(0, alive_soldiers.length-1);
			var s = alive_soldiers[_index];
			if (s) {
			    var pos = {x: s.pos.x, y: s.pos.y};
				s.kill();
				s.pos = pos;
			}
			alive_soldiers.splice(_index, 1);			
		}		
	},
	recoverSoldier: function(side, quantity) {
        var soldiers = this.up_army;
        var y = -30;
        if (side == "down") {
            soldiers = this.down_army;
            y = ig.system.height;
        }
        var i = 0;
        var dead_soldiers = [];
        for (i =0; i < soldiers.length; i++) {
            if (soldiers[i]._killed) {
                dead_soldiers.push(soldiers[i]);
            }
        }
        for (i = 0; i < quantity; i++) {
            var _index = getRandomInt(0, dead_soldiers.length-1);
            var s = dead_soldiers[_index];
            if (s) {
                var pos = {x: s.pos.x, y: y};
                s.reset();
                s.pos = pos;
                this.entities.push(s);
                s.moveForward(50);
            }
            dead_soldiers.splice(_index, 1);           
        }
    },
	takeDamage: function(side, amount) {
		var hp_bar = this.up_health_bar;
		if (side == "down") {
			hp_bar = this.down_health_bar;
		}				
		this.drawBullets();
		var _this = this;
		setTimeout(
			function() {
				//hp_bar.current_hp -= amount;
				_this.drawExplosion(side, amount);
			},
			500
		);
		setTimeout(
				function() {
					_this.dieSoldier(side, Math.round(amount/10));
				},
			1000
		);
	},
	takeReinforcement: function(side, amount) {
	    this.recoverSoldier(side, Math.round(amount/10));
	},
	
	drawConfirmDialog: function() {
	   var dialog = this.spawnEntity(DialogEntity, 0, 0);
	   dialog.pos.x = (ig.system.width - dialog.size.x)/2;
	   dialog.pos.y = (ig.system.height - dialog.size.y)/2;
	   dialog.text = "Continue?";   
	   this.confirm_dialog = dialog;
	   
	},
	closeConfirmDialog: function() {
		if (this.confirm_dialog) {
		   this.confirm_dialog.kill();
		   this.confirm_dialog = null;
		}		   
	},
	
	update: function() {
		// Update all entities and backgroundMaps
		this.dealCards();
		var delta = this.timer.delta();
		if (delta < 0) {
		    if (this.time_bar) {
		        this.time_bar.setScale(Math.abs(delta)/TURN_WAITING_TIME, 1);
		    }
		}
		this.parent();
		if( ig.input.pressed('call') ) {
			GAME.bet_call_or_check();
		}
		if( ig.input.pressed('raise') ) {
            GAME.bet_raise();
        }
        if( ig.input.pressed('fold') ) {
            GAME.bet_fold();
        }
		if( ig.input.pressed('exit') ) {
			this.sounds.click.play();
			GAME.partRoom();
		}
		if (this.confirm_dialog) {
		    if (ig.input.pressed('ready')) {
		    	this.sounds.click.play();
		        GAME.readyRoom();
		        this.closeConfirmDialog();
		    }
		}
		
	},
	
	draw: function() {
		// Draw all entities and backgroundMaps
		this.parent();			
		if( this.buttons && (!this.waiting) ) {
            this.buttons.draw(); 
        }
        if (this.confirm_dialog) {
           if (this.confirm_button) {
               this.confirm_button.draw();
           } 
        }
        
        if (this.waiting) {
            var r = Math.random();
            if (r<0.005) {
                this.drawBombing();
            }
            if (!this.confirm_dialog) {
                this.waiting_text.draw('Please wait for other player...', 
                                        ig.system.width/2, 
                                        ig.system.height/2, 
                                        ig.Font.ALIGN.CENTER);
            }
        }
        if (this.exit_button) {
            this.exit_button.draw();
        }
	}
});

});

