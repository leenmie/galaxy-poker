ig.module( 
    'game.start' 
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
    
StartGame = ig.Game.extend({ 
    background_image: new ig.Image('media/graphics/interface/background_menu.png'),
    click_sound: new ig.Sound('media/sounds/ready.ogg'),
    font: new ig.Font('media/freemono.font.png'),
    init: function() {
        this.init_input();
    },
    init_input: function() {
        ig.input.bind( ig.KEY.ENTER, 'join_room' );
        var image_button_play = new ig.Image('media/graphics/interface/button_play.png');
        var image_button_quit = new ig.Image('media/graphics/interface/button_quit.png');
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
            new ig.TouchButton( 'join_room', {left: (ig.system.width - 112)/2, top: 200}, 112, 112, image_button_play, 0 ),
            new ig.TouchButton( 'log_out', {left: 3, top: 408}, 40, 40, image_button_quit, 0 ),
            new ig.TouchButton( 'music', {left: 598, top: 408}, 40, 40, image_music, 0 )
        ]);
            
        this.buttons.align();       
    }, 
    update: function() {
        this.parent();
        if (!this.waitForResponse) {
            if(ig.input.pressed('join_room')) {
            	this.click_sound.play();
                if (GAME) {
                    if (GAME.userinfo) {
                        GAME.joinRoom();
                    }
                }                
                this.wait(3);
            }
            if(ig.input.pressed('log_out')) {
                this.click_sound.play();
                if (GAME) {
                    GAME.logOut();
                }
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
        if (GAME) {
            if (GAME.loginFailed) {
                GAME.loginScene();
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
        this.font.draw("Start", 320, 50, ig.Font.ALIGN.CENTER);
    }
});

});
