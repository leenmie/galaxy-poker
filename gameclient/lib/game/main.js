ig
.module('game.main')
.requires(
    'game.menu',
    'game.play',
    'plugins.splash-loader'
)
.defines(function(){
    //ig.main('#canvas', MenuGame, 30, 320, 240, 1, ig.SplashLoader);   
    ig.System.scaleMode = ig.System.SCALE.CRISP;
    ig.main('#canvas', MenuGame, 30, 320, 240, 1, ig.SplashLoader);     
});