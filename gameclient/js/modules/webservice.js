define(["config","../../appframework/appframework"], function(mod_config) {
    return {
        authenticate : function(username, password, funcCallback, errorCallback) {
            jq.ajax({
                url : mod_config.webservice.base_url + "/authenticate",
                cache : false,
                type : "POST",
                dataType : "json",
                data : {
                    "email" : username.toLowerCase(),
                    "password" : password
                },
                error : function(jqXHR, textStatus, errorThrown) {
                    errorCallback();
                    console.log("Error when call authenticate service", jqXHR);
                },
                success : function(data, textStatus, jqXHR) {
                    var result = data;
                    console.log("Authenticate result", data);
                    funcCallback(result);
                },
            });
            return true;
        },
        anonymous: function(funcCallback, errorCallback) {
            jq.ajax({
                url : mod_config.webservice.base_url + "/anonymous",
                cache : false,
                type : "POST",
                dataType : "json",
                data : null,
                error : function(jqXHR, textStatus, errorThrown) {
                    errorCallback();
                    console.log("Error when call anonymous service", jqXHR);
                },
                success : function(data, textStatus, jqXHR) {
                    var result = data;
                    console.log("Anonymous result", data);
                    funcCallback(result);
                },
            });
            return true;
        },
        register : function(username, password, funcCallback, errorCallback) {
            jq.ajax({
                url : mod_config.webservice.base_url + "/register",
                cache : false,
                type : "POST",
                dataType : "json",
                data : {
                    "email" : username.toLowerCase(),
                    "password" : password
                },
                error : function(jqXHR, textStatus, errorThrown) {
                    errorCallback();
                    console.log("Error when call register service", jqXHR);
                },
                success : function(data, textStatus, jqXHR) {
                    var result = data;
                    console.log("Register result", data);
                    funcCallback(result);
                },
            });
            return true;
        },
        userinfo: {
            get: function(sessiontoken, guestid, funcCallback, errorCallback) {
                jq.ajax({
                    url : mod_config.webservice.base_url + "/userinfo",
                    cache : false,
                    type : "GET",
                    dataType : "json",
                    data : {
                        "sessiontoken" : sessiontoken,
                        "guestid" : guestid
                    },
                    error : function(jqXHR, textStatus, errorThrown) {
                        errorCallback();
                        console.log("Error when get userinfo", jqXHR);
                    },
                    success : function(data, textStatus, jqXHR) {
                        var result = data;                       
                        funcCallback(result);
                    },
                });
                return true;
            },
            update: function(sessiontoken, guestid, avatar, nickname, oldpassword, newpassword, funcCallback, errorCallback) {
                jq.ajax({
                    url : mod_config.webservice.base_url + "/userinfo",
                    cache : false,
                    type : "POST",
                    dataType : "json",
                    data : {
                        "sessiontoken" : sessiontoken,
                        "guestid" : guestid,
                        "avatar": avatar,
                        "nickname": nickname,
                        "oldpassword": oldpassword,
                        "newpassword": newpassword,
                    },
                    error : function(jqXHR, textStatus, errorThrown) {
                        errorCallback();
                        console.log("Error when update userinfo", jqXHR);
                    },
                    success : function(data, textStatus, jqXHR) {
                        var result = data;                       
                        funcCallback(result);
                    },
                });
                return true;
            },
        },
        facebook_login : function(access_token, funcCallback, errorCallback) {
            jq.ajax({
                url : mod_config.webservice.base_url + "/fblogin",
                cache : false,
                type : "POST",
                dataType : "json",
                data : {
                    'accesstoken' : access_token,
                },
                error : function(jqXHR, textStatus, errorThrown) {
                    errorCallback();
                    console.log("Error when call fblogin service", jqXHR);                    
                },
                success : function(data, textStatus, jqXHR) {
                    var result = data;
                    //console.log(result);
                    if (result['result'] == 0) {//success
                        //var token = result['authenticated_token'];                        
                        //mod_utils.save_login_session(username, token);
                        if (funcCallback) {
                            funcCallback(result);
                        }
                    } else {
                        errorCallback();
                    }
                },
            });            
        },                  
    }; 
});
