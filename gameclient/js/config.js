define([],function() {
    return {
        MAX_HEIGHT: 768,
        ORIGINAL_WIDTH: 640,
        ORIGINAL_HEIGHT: 480,
        
        /*webservice: {
            base_url: 'http://localhost/service/',
        },
        xmpp: {
            http_base: 'http://localhost/http-bind/',
            domain: 'ubuntu',
            resource: 'texaspoker_web',
            host: 'ubuntu',
            game_server: 'game.ubuntu',
        },*/
       webservice: {            
            base_url: 'http://cacafefe.com/service/',            
        },
        xmpp: {            
            http_base: 'http://cacafefe.com/http-bind/',
            domain: 'cacafefe.com',
            resource: 'texaspoker_web',
            host: 'cacafefe.com',
            game_server: 'galaxypoker.cacafefe.com',
        },
    };
});
