ig.module(
	'plugins.splash-loader'
)
.requires(
	'impact.loader',
	'game.entities'
)
.defines(function(){

ig.SplashLoader = ig.Loader.extend({
	
	endTime: 0,
	fadeToWhiteTime: 200,
	fadeToGameTime: 800,
	logoWidth: 340,
	logoHeight: 120,
	logo: document.getElementById("splash-logo"),
	/*load: function() {
		try {
			this.parent();
		}
		catch (e) {
			//do nothing
			console.log('Loader err');
			this.end();
			return;
		}
	},*/
	end: function() {
		this.parent();
		this.endTime = Date.now();
		
		// This is a bit of a hack - set this class instead of ig.game as the delegate.
		// The delegate will be set back to ig.game after the screen fade is complete.
		ig.system.setDelegate( this );
	},
	
	
	// Proxy for ig.game.run to show the screen fade after everything is loaded
	run: function() {	
		var t = Date.now() - this.endTime;
		var alpha = 1;
		if( t < this.fadeToWhiteTime ) {
			// Draw the logo -> fade to white
			this.draw();
			alpha = t.map( 0, this.fadeToWhiteTime, 0, 1);
		}
		else if( t < this.fadeToGameTime ) {
			// Draw the game -> fade from white
			ig.game.run();
			alpha = t.map( this.fadeToWhiteTime, this.fadeToGameTime, 1, 0);
		}
		else {
			// All done! Dismiss the preloader completely, set the delegate
			// to ig.game
			ig.system.setDelegate( ig.game );
			return;
		}
		
		// Draw the white rect over the whole screen
		ig.system.context.fillStyle = 'rgba(255,255,255,'+alpha+')';
		ig.system.context.fillRect( 0, 0, ig.system.realWidth, ig.system.realHeight );
	},
	
	
	draw: function() {
		// Some damping for the status bar
		this._drawStatus += (this.status - this._drawStatus)/5;
		
		var ctx = ig.system.context;
		var w = ig.system.realWidth;
		var h = ig.system.realHeight;
		var scale = w / this.logoWidth / 3; // Logo size should be 1/3 of the screen width
		var center = (w - this.logoWidth * scale)/2;
		
		// Clear
		ctx.fillStyle = 'rgba(0,0,0,0.8)';
		ctx.fillRect( 0, 0, w, h );
		
		// URL
		ctx.fillStyle = 'rgb(128,128,128)';
		ctx.textAlign = 'right';
		ctx.font = '10px Arial';
		ctx.fillText( 'Galaxy Poker', w - 10, h - 10 );
		ctx.textAlign = 'left';		
		ctx.save();		
		
        ctx.translate( center, h / 2.5 );
        ctx.scale( scale, scale );        
        // Loading bar ('visually' centered for the Impact logo)
        ctx.lineWidth = '3';
        ctx.strokeStyle = 'rgb(255,255,255)';
        ctx.strokeRect( 25, this.logoHeight + 40, 300, 20 );
        
        ctx.fillStyle = 'rgb(255,255,255)';
        ctx.fillRect( 30, this.logoHeight + 45, 290 * this._drawStatus, 10 );							
		ctx.restore();		
        ctx.drawImage(this.logo, ig.system.width * this._drawStatus, 10);
	}	
});

});
