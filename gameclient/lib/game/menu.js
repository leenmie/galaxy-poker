ig.module( 
	'game.menu' 
)
.requires(
	'impact.game',
	'impact.font',
	'impact.input',
	'impact.background-map',
	'plugins.touch-button',
	'plugins.wait-game',
	'game.play'
)
.defines(function(){
	
MenuGame = ig.Game.extend({	
	background_image: new ig.Image('media/graphics/interface/background_menu.png'),
	click_sound: new ig.Sound('media/sounds/ready.ogg'),
	font: new ig.Font('media/freemono.font.png'),
	init: function() {
		this.init_input();
	},
	init_input: function() {
		ig.input.bind( ig.KEY.LEFT_ARROW, 'guest_login' );
		ig.input.bind( ig.KEY.RIGHT_ARROW, 'facebook_login' );		
		var image_button_guest = new ig.Image('media/graphics/interface/button_guest.png');
		var image_button_facebook = new ig.Image('media/graphics/interface/button_facebook.png');
		var image_button_music = new ig.Image('media/graphics/interface/button_music.png');
        var image_button_music_mute = new ig.Image('media/graphics/interface/button_music_mute.png');
        var image_music = null;
        if (ig.music.muted) {
        	image_music = image_button_music_mute;        	
        }
        else {
        	image_music = image_button_music;
        }
		this.buttons = new ig.TouchButtonCollection([
			new ig.TouchButton( 'guest_login', {left: 200, top: 200}, 100, 100, image_button_guest, 0 ),
			new ig.TouchButton( 'facebook_login', {right: 200, top: 200}, 100, 100, image_button_facebook, 0 ),
			new ig.TouchButton( 'music', {left: 598, top: 408}, 40, 40, image_music, 0 )
		]);
            
		this.buttons.align();		
	},	
	update: function() {
		this.parent();
		if (!this.waitForResponse) {
    		if (ig.input.pressed('guest_login')) {
    			//console.log('left pressed');
    			//ig.system.setGame(PokerGame);
    			this.click_sound.play();
    			loginGuest();    			
    			this.wait(3);
    		}
    		if (ig.input.pressed('facebook_login')) {
    			this.click_sound.play();
    		    loginFacebook();    		    
    		    this.wait(3);
    		}
            if(ig.input.pressed('music')) {
                if (ig.music.muted) {
                	var image_button_music = new ig.Image('media/graphics/interface/button_music.png');
                	var button = this.buttons.buttons[2];
                	button.image = image_button_music;
                	ig.music.play();
                	ig.music.muted = false;
                }
                else {
                	var image_button_music_mute = new ig.Image('media/graphics/interface/button_music_mute.png');
                	var button = this.buttons.buttons[2];
                	button.image = image_button_music_mute;
                	ig.music.stop();
                	ig.music.muted = true;
                }                
            }    		
		}
	},
	draw: function() {
		this.parent();
		if (this.background_image) {
			this.background_image.draw(0, 0);
		}
		if( this.buttons ) {
            this.buttons.draw(); 
        }
		this.font.draw("Login", 320, 50, ig.Font.ALIGN.CENTER);
		this.font.draw("Guest", 250, 310, ig.Font.ALIGN.CENTER);
		this.font.draw("Facebook", ig.system.width - 250, 310, ig.Font.ALIGN.CENTER);
	}
});

});
