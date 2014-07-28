ig.module(
    'plugins.wait-game'
)
.requires(
    'impact.game'
)
.defines(function(){
ig.Game.inject({
    waitForResponse: false,    
    wait: function(seconds) {
        this.waitForResponse = true;
        var _this = this;
        setTimeout(function() {
            _this.waitForResponse = false;
        }, seconds*1000);
    }
});
    
});