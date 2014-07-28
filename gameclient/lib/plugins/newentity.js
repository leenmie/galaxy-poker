/*
 * Scale Individual Entities Plugin
 * Written By Abraham Walters
 * June 2012
 * Corrected By Leen
 * April 2014
 */
ig.module(
    'plugins.newentity'
)
.requires(
    'impact.entity'
)
.defines(function(){
 
ig.Entity.inject({

    scale: { x: 1, y: 1 },      //user-defined scale
    _original_offset: { x: 0, y: 0 },    //cached offset prior to scaling
    _original_size: { x: 0, y: 0 },      //cached size prior to scaling
    init: function( x, y, settings ){
        this.parent( x, y, settings );
        this._original_offset.x = this.offset.x;
        this._original_offset.y = this.offset.y;
        this._original_size.x = this.size.x;
        this._original_size.y = this.size.y;
        this.setScale( this.scale.x, this.scale.y );
    },
 
    draw: function(){
        var ctx = ig.system.context;
        ctx.save();
        ctx.translate(
            ig.system.getDrawPos( this.pos.x.round() - this.offset.x - ig.game.screen.x ),
            ig.system.getDrawPos( this.pos.y.round() - this.offset.y - ig.game.screen.y )
        );
        ctx.scale( this.scale.x, this.scale.y );
        if (this.currentAnim) {
        	this.currentAnim.draw( 0, 0 );
        }
        ctx.restore();
    },
	
	moveTo: function(to_x, to_y, duration){	
		if (!duration) {
			duration = 0.1;
		}		
		var move_x = (to_x - this.pos.x) / duration;
		var move_y = (to_y - this.pos.y) / duration;		
		this.maxVel.x = Math.abs(move_x);
		this.maxVel.y = Math.abs(move_y);				
		this.vel.x = move_x;
		this.vel.y = move_y;
		var _this = this;
		setTimeout(function() {
			_this.stopMoving(to_x, to_y);
		}, duration * 1000 + 10);
		return this;
	},
	
	stopMoving: function(x, y) {
		this.vel.x = 0;
		this.vel.y = 0;
		this.pos.x = x;
		this.pos.y = y;
	},
	
	update: function() {
		this.parent();
	},
	
    setScale: function( x, y ){
        //cache size prior to scaling
        var oX = this.size.x, 
            oY = this.size.y;

        //set scale
        this.scale.x = x;
        this.scale.y = y;


        //scale offset
        this.offset.x = this._original_offset.x * this.scale.x;
        this.offset.y = this._original_offset.y * this.scale.y;

        //scale size
        this.size.x = this._original_size.x * this.scale.x;
        this.size.y = this._original_size.y * this.scale.y;

        //offset entity's position by the change in size
        //this.pos.x += (oX - this.size.x) / 2;
        //this.pos.y += (oY - this.size.y) / 2; 
    }
 
});
 
});
