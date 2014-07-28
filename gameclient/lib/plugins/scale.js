/*
 * Scale Individual Entities Plugin
 * Written By Abraham Walters
 * June 2012
 * Corrected By Leen
 * April 2014
 */
ig.module(
    'plugins.scale'
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
        this.currentAnim.draw( 0, 0 );
        ctx.restore();
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