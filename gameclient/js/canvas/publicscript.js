/*
 * public API in order to call between webview and cocoonjs
 */

function loginSuccessful(json_userinfo) {
    var userinfo = JSON.parse(json_userinfo);
    GAME.userinfo = userinfo;
    GAME.loginFailed = false;
    GAME.startScene();
    console.log(userinfo);
}

function loginFailed() {
    GAME.loginFailed = true;
    //GAME.loginScene();
    console.log('login failed.');
}

function sendCommand(cmd) {
    var json_message = JSON.stringify(cmd);
    json_message = "'" + json_message + "'";
    var command = "sendXMPPMessage(" + json_message + ");";
    //console.log(command);
    CocoonJS.App.forwardAsync(command);
}

function receiveServerCommand(message) {
    GAME.receiveServerCommand(message);
    //console.log(message);
}

function showEditProfile() {
    require(["utils/transformCalculator"], function(transformCalculator) {
        var left_corner = transformCalculator.left_corner;
        var director = global_director;
        var wv_width = Math.floor(director.width * 0.9);
        var wv_height = Math.floor(director.height * 0.9);
        var wv_pos = {x: (director.width - wv_width)/2 + left_corner.x,
                       y: (director.height -wv_height)/2 + left_corner.y};          
        CocoonJS.App.forwardAsync("showUp("+wv_pos.x+","+wv_pos.y+","+director.width+","+director.height+",0.9, '#edit_profile');", function(){});
    });    
}

function loginGuest() {
    var command = "loginAnonymous();";
    var anon = CocoonJS.App.forwardAsync(command, function(){});    
}

function loginFacebook_native() {
    var FACEBOOK_PARAMS = {
	    appId      : '662073747195419',
	    channelUrl : '/galaxy/channel.html',
	    status : true, // Check Facebook Login status
	    xfbml : true // Look for social plugins on the page
    };
    function Facebook_init(fbparams) 
    {
        var socialServiceFB = CocoonJS.Social.Facebook;
        socialServiceFB.init(fbparams);
        socialServiceFB.getLoginStatus(function(response) {
        	if (response.status != "connected") {
                socialServiceFB.login(function(authResponse) {
                    if (response.authResponse) {
                    	var access_token = authResponse.accessToken;
                    	console.log(access_token);
                    	var command = 'loginFacebook("'+access_token+'");';                        
                        CocoonJS.App.forwardAsync(command);
                    } 
                    else {
                        // cancelled
                        console.log('Facebook login cancelled.');
                    }
                });    
            }
            else {
            	var access_token = socialServiceFB._currentSession.authResponse.accessToken;
            	var command = 'loginFacebook("'+access_token+'");';
            	console.log(command);
            	CocoonJS.App.forwardAsync(command);            	
            }        	
        });
        
    }
    Facebook_init(FACEBOOK_PARAMS);    
}
loginFacebook = loginFacebook_native;
