/**
 * Public function to communicate between 2 contexts
 */

require(
		[
		 "modules/xmppConnection", 
         "modules/webservice",
         "modules/session",
		 ], 
		function
		(
		xmpp_connection, 
		mod_webservice,
		mod_session
		) 
{
			
XMPP_CONNECTION = xmpp_connection;
XMPP_CONNECTION.actionLoginFailed = function() {
	logOutSession();
};
			
forwardUserInfo = function(userinfo) {
    USER_INFO = userinfo;
    //console.log(USER_INFO);
    //console.log('forwardUserInfo');
    json_string = "'"+JSON.stringify(userinfo)+"'";
    command = "loginSuccessful("+json_string+");";
    CocoonJS.App.forwardAsync(command, function(){});
};

loginXMPP = function(email, password) {        
    var callbackUserInfo = function(data) {
        var userinfo = data['userinfo'];
        forwardUserInfo(userinfo);
    };
    var callbackFunc = function(data) {    
        var user = data['userid'];
        var pass = data['authenticated_token'];
        console.log('Login XMPP', user, pass);
        XMPP_CONNECTION.actionConnected = function() {
            saveSession({userid: user, password: pass});
            mod_webservice.userinfo.get(pass, null, callbackUserInfo, errFunc);
        };
        var connected = XMPP_CONNECTION.doSessionLogin(user, pass);
    };
    var errFunc = function(data) {
        alert('Cannot connect to server');
    };
    mod_webservice.authenticate(email, password, callbackFunc, errFunc);
};

refreshUserInfo = function(password, username) {
    var callbackUserInfo = function(data) {
        var userinfo = data['userinfo'];
        forwardUserInfo(userinfo);
    };
    var errCallback = function() {
        console.log('Webservice error');
    };
    if (username.indexOf('guest') >= 0) {
        mod_webservice.userinfo.get('guest', username, callbackUserInfo, errCallback);
    } else {
        mod_webservice.userinfo.get(password, null, callbackUserInfo, errCallback);
    }
};

loginAnonymous = function() {        
    var callbackUserInfo = function(data) {
        var userinfo = data['userinfo'];
        forwardUserInfo(userinfo);
    };
    var funCallback = function(data) {
        var username = data['userid'];
        var password = 'guest'; //guest account, password is not provided
        console.log('Guest account: ',username);
        XMPP_CONNECTION.actionConnected = function() {
            saveSession({userid: username, password: 'guest'});
            mod_webservice.userinfo.get('guest', username, callbackUserInfo, errCallback);
        };
        var connected = XMPP_CONNECTION.doSessionLogin(username, password);                         
    };
    var errCallback = function() {
        console.log('Webservice error');
    };
    var session = mod_session.get();
    if (session) {
         var resume = resumeSession(session);
    }
    if (!resume) {
        mod_webservice.anonymous(funCallback, errCallback);
    }
};

loginFacebook = function(access_token) {
    var callbackUserInfo = function(data) {
        var userinfo = data['userinfo'];
        forwardUserInfo(userinfo);
    };
    var callbackFunc = function(data) {
        if (data['result']!=0) {
            alert('Facebook login error');
            return;
        }    
        var user = data['userid'];
        var pass = data['authenticated_token'];
        console.log('Login XMPP', user, pass);
        XMPP_CONNECTION.actionConnected = function() {
            saveSession({userid: user, password: pass});
            mod_webservice.userinfo.get(pass, null, callbackUserInfo, errCallback);
        };
        var connected = XMPP_CONNECTION.doSessionLogin(user, pass);
    };
    var errCallback = function(result) {
        alert('Facebook login error');    
    };
    mod_webservice.facebook_login(access_token, callbackFunc, errCallback);               
};

resumeSession = function(session) {
    var username = session['userid'];
    var password = session['password'];
    var callbackUserInfo = function(data) {
        var userinfo = data['userinfo'];
        forwardUserInfo(userinfo);
    };
    var errCallback = function() {
        CocoonJS.App.forwardAsync("loginFailed();", function(){});
    };
    XMPP_CONNECTION.actionConnected = function() {
        refreshUserInfo(password, username);
    };
    XMPP_CONNECTION.actionDisconnected = function() {
        CocoonJS.App.forwardAsync("loginFailed();", function(){});
        console.log("XMPP disconnected");
    };
    var connected = XMPP_CONNECTION.doSessionLogin(username, password);                                    
    return connected;
};

saveSession = function(session) {
    mod_session.set(session);
};

logOutSession = function() {
    XMPP_CONNECTION.quit();
    mod_session.clear();
    console.log('Log out');
};

sendXMPPMessage = function(body) {
    XMPP_CONNECTION.sendCommand(body);
};

updateUserInfo = function () {
    var session = mod_session.get();
    var username = session['userid'];
    var token = session['password'];
    if (username.indexOf('guest')<0) {
        username = "";
    }
    var avatar = SELECTED_AVATAR;
    var oldpassword = af('#input_oldpassword').val();
    var newpassword = af('#input_newpassword').val();
    var nickname = af('#input_nickname').val();
    var successCallback = function (result) {
        hideOut();
        refreshUserInfo(token, username);                        
    };
    var failedCallback = function () {
        alert('failed');
    };
    console.log(avatar, oldpassword, newpassword);
    mod_webservice.userinfo.update(token, username, avatar, nickname,
        oldpassword, newpassword, successCallback, failedCallback);    
};

checkSavedSession = function () {
    var session = mod_session.get();
    if (session) {
         return resumeSession(session);
    }
    else {
        CocoonJS.App.forwardAsync("loginFailed();", function(){});
    }    
    return false;
};
			
}
);