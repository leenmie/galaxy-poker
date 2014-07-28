require.config({
    urlArgs: "bust=" + (new Date()).getTime(),
});
require(
    [
    'vendor/cocoon',
    'canvas/publicscript',
    'modules/GameTexasPokerClient',
    '../lib/impact/impact',    
    'config'
    ], 
    function
    (
    	lib_cocoon,
        publicscript,
        GameTexasPokerClient,
        lib_impact, 
        config
    ) 
{    	
    GAME = new GameTexasPokerClient();    
    ig
    .module('game.main')
    .requires(
        'game.menu',
        'game.play',
        'game.start',
        'plugins.splash-loader'
    )
    .defines(function(){
        //ig.main('#canvas', PokerGame, 30, config.ORIGINAL_WIDTH, config.ORIGINAL_HEIGHT, 1, ig.SplashLoader);
        ig.main('#canvas', StartGame, 30, config.ORIGINAL_WIDTH, config.ORIGINAL_HEIGHT, 1, ig.SplashLoader);
        ig.music.add('media/music/giai_phong_quan.ogg');
        ig.music.add('media/music/hat_mai_khuc_quan_hanh.ogg');
        ig.music.volume = 0.3;
        //ig.music.play();
        ig.music.muted = true;
    });
    
}
);
