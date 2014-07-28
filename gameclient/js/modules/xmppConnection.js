define(["vendor/jsjac", "config"], function(jsjac, mod_config) {
    return {
        httpBase : mod_config.xmpp.http_base,
        domain : mod_config.xmpp.domain,
        con : null,
        doSessionLogin : function(username, password) {
            try {
                // setup args for contructor
                var oArgs = new Object();
                oArgs.httpbase = this.httpBase;
                oArgs.timerval = 2000;

                this.con = new JSJaCHttpBindingConnection(oArgs);

                this.setupCon();
                // setup args for connect method
                oArgs = new Object();
                oArgs.domain = mod_config.xmpp.domain;
                oArgs.username = username.toLowerCase();
                oArgs.resource = mod_config.xmpp.resource;
                oArgs.pass = password;
                oArgs.register = false;
                //data['register'];
                oArgs.host = mod_config.xmpp.host;
                this.con.connect(oArgs);
            } catch (err) {
                this.onError(err);
                //console.log(err);
                return false;
            }
            return true;
        },
        init : function() {
            try {// try to resume a session
                if (JSJaCCookie.read('btype').getValue() == 'binding')
                    this.con = new JSJaCHttpBindingConnection({
                        'oDbg' : oDbg
                    });
                if (this.con.resume()) {
                    this.onResume();
                }
                this.setupCon(this.con);
            } catch (e) {
            } // reading cookie failed - never mind
        },
        setupCon : function() {
            this.con.registerHandler('message', this.handleMessage);
            this.con.registerHandler('presence', this.handlePresence);
            this.con.registerHandler('iq', this.handleIQ);
            this.con.registerHandler('status_changed', this.handleStatusChanged);

            this.con.registerHandler('onerror', this.handleError);
            this.con.registerHandler('onconnect', this.handleConnected);
            this.con.registerHandler('ondisconnect', this.handleDisconnected);
            this.con.registerIQGet('query', NS_VERSION, this.handleIqVersion);
            this.con.registerIQGet('query', NS_TIME, this.handleIqTime);
        },
        handleMessage : function(aJSJaCPacket) {
            var from = aJSJaCPacket.getFrom();
            if (from != mod_config.xmpp.game_server) {
                console.log('Receiving message from other user is not implemented.');
                return;
            }
            var message = aJSJaCPacket.getBody();
            //console.log('Received: ', message);
            var msgs = message.split('\n');
            //console.log(msgs);
            for (var i=0; i<msgs.length; i++) {
                var command = "receiveServerCommand('"+msgs[i]+"');";
                //console.log(command);
                try{        
                    CocoonJS.App.forwardAsync(command,function(){});
                }
                catch (e) {
                    console.log(e, e.message);
                }
            }            
        },
        handlePresence : function() {
        },
        handleIQ : function() {
        },
        handleStatusChanged : function() {
        },
        handleError : function(e) {
            console.log('handleError', e);
            var _this = XMPP_CONNECTION;
            if (e.attributes['code'].value == "401" && e.attributes['type'].value == 'auth') {
            	_this.actionLoginFailed();
            }
            else if (e.attributes['code'].value == "500" && e.attributes['type'].value == 'cancel') {
            } 
            else if (e.attributes['code'].value == "503" && e.attributes['type'].value == 'cancel') {
                try {                    
                    _this.actionDisconnected();            
                }
                catch (err) {
                    console.log(err.message);
                }                
            } 
            else {
                //alert('Unhandle error.');
            }
        },
        handleConnected : function() {
            console.log('XMPP Connected');
            var _this = XMPP_CONNECTION;            
            _this.actionConnected();            
            _this.con.send(new JSJaCPresence());            
        },
        handleDisconnected : function() {
            CocoonJS.App.forwardAsync("loginFailed();", function(){});
            //alert('Connection is broken.');
        },
        handleIqVersion : function(iq) {
            var _this = XMPP_CONNECTION;
            _this.con.send(iq.reply([iq.buildNode('name', 'jsjac simpleclient'), iq.buildNode('version', JSJaC.Version), iq.buildNode('os', navigator.userAgent)]));
            return true;
        },
        handleIqTime : function(iq) {
            var now = new Date();
            var _this = XMPP_CONNECTION;
            _this.con.send(iq.reply([iq.buildNode('display', now.toLocaleString()), iq.buildNode('utc', now.jabberDate()), iq.buildNode('tz', now.toLocaleString().substring(now.toLocaleString().lastIndexOf(' ') + 1))]));
            return true;
        },
        onResume : function() {
            alert('connection resume');
        },
        onError : function(e) {
            console.log('onError',e);
            /*if (this.con && this.con.connected())
             this.con.disconnect();*/
            return false;
        },
        quit : function() {
            var p = new JSJaCPresence();
            p.setType("unavailable");
            this.con.send(p);
            this.con.disconnect();
        },
        onUnload : function() {
            var _this = XMPP_CONNECTION;
            if ( typeof _this.con != 'undefined' && _this.con && _this.con.connected()) {
                // save backend type
                if (_this.con._hold)// must be binding
                    (new JSJaCCookie('btype', 'binding')).write();
                if (_this.con.suspend) {
                    _this.con.suspend();
                }
            }
        },
        sendCommand : function(msg, callbackFunction) {
            try {
                var aMsg = new JSJaCMessage();
                aMsg.setTo(new JSJaCJID(mod_config.xmpp.game_server));
                aMsg.setType('chat');
                aMsg.setBody(msg);
                //            alert(msg);
                var response = this.con.send(aMsg);
                if (response) {
                    if (callbackFunction) {
                        callbackFunction.call();
                    }
                }
            } catch (e) {
                console.log('XMPP error send msg', e);
                return false;
            }
            return true;
        },
        actionConnected : function() {            
            //we add this action later
        },
        actionDisconnected: function() {
            
        },
        actionLoginFailed: function() {
        	
        }
    };
});
