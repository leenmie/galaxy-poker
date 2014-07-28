/**
 * Game logic engine
 */
define(
		[
		"vendor/cocoon", 
        "modules/player",
        "config"
        ], 
        function
        (
        lib_cocoon,
        player,
        config
        ) 
{
	function GameTexasPokerClient() {
		this.init();
	};
	
	GameTexasPokerClient.prototype.init = function() {
		this.director = null;
		this.player = player;
		this.loginFailed = false;
		this.message_queue = [];
		this.running_loop = false;
		this.pause_processing = false;
		/*these game information updated from server */
	    this.gamestatus = -1;
	    this.userlist = [];
	    this.readylist = [];
	    this.big_blind = null;
	    this.small_blind = null;
	    this.big_blind_amount = 0;
	    this.my_pot = 0;
	    this.enemy_pot = 0;
        this.default_stake = 0;
	    this.my_stake = 0;
	    this.enemy_stake = 0;
	    this.current_round = 0;
	    	
		this.game = null;
		this._loadWebView();	
		this._initCanvas();	
	};
	
	GameTexasPokerClient.prototype._initCanvas = function() {
        var canvas = document.getElementById('canvas');
        var height = window.innerHeight;
        var width = window.innerWidth;
        if (height > config.MAX_HEIGHT) {
        	height = config.MAX_HEIGHT;
        }
        var rate = width/height;
        if (rate < 1.2) {
            height = width / 1.2;
        }
        if (rate > 1.7) {
            width = height * 1.7;
        }
        canvas.setAttribute('style', 'position: relative; left:'+ (window.innerWidth - width)/2 + 'px');
        canvas.style.width = width + 'px';
        canvas.style.height = height + 'px';
	};
		
	GameTexasPokerClient.prototype._loadWebView = function() {
        CocoonJS.App.onLoadInTheWebViewSucceed.addEventListener(function() {
            CocoonJS.App.forwardAsync("waitForLoading();", function(){});                        
        });
        CocoonJS.App.loadInTheWebView("webview.html");		
	};
	

    GameTexasPokerClient.prototype.startScene = function () {
        this.game = null;
        ig.system.setGame(StartGame);        
    };
    
    GameTexasPokerClient.prototype.loginScene = function () { 
        this.game = null;       
        ig.system.setGame(MenuGame);                       
    };
    
    GameTexasPokerClient.prototype.playScene = function () {        
        ig.system.setGame(PokerGame);
        //this.game = ig.game;
    };

    GameTexasPokerClient.prototype.receiveServerCommand = function (json_message) {
    	var message = null;
    	try {
    		message = JSON.parse(json_message);
    	}
    	catch (e) {
    		return;
    	}
    	//console.log(message);
    	if (message) {
    		this.message_queue.push(message);    
    	}
    };
    
    GameTexasPokerClient.prototype.processMessage = function() {
        var message = this.message_queue.shift();
        if (!message) {
            return;
        }
        console.log(message);
        
        var command = message["command"];
        if (command == "join") {
            this.processJoin(message);
        }
        else if (command == "part") {
            this.processPart(message);
        }
        else if (command == "gamestatus") {
            this.gamestatus = message["status"];
        }
        else if (command == "userlist") {
            this.userlist = message["list"];
            this._sortUserlist();
        }
        else if (command == "readylist") {
            this.readylist = message["list"];
        }
        else if (command == "startgame") {
            this.processStartGame(message);
        }
        else if (command == "bet") {
            this.processBet(message);
        }
        else if (command == "fold") {
            this.processFold(message);
        }
        else if (command == "deal") {
            this.processDeal(message);
        }
        else if (command == "turn") {
            this.processTurn(message);
        }
        else if (command == "stake") {
            this.processStake(message);
        }
        else if (command == "deal_community") {
            this.processDealCommunity(message);
        }
        else if (command == "stopgame") {
            this.processStopGame();
        }
        else if (command == "submit") {
            this.processSubmit(message);
        }
        else if (command == "winner") {
            this.processWinner(message);
        }
        else if (command == "stopmatch") {
            this.processStopMatch(message);
        }                
        
    };
    
    GameTexasPokerClient.prototype._sortUserlist = function() {
        /*make sure our username is always at 0 index */
        for (var i=0; i< this.userlist.length; i++) {
            if (this.userlist[0]["username"]!=this.userinfo.userid) {
                var user = this.userlist.shift();
                this.userlist.push(user);
                break;    
            }
        }
    };
    
    GameTexasPokerClient.prototype.loopProcessMessage = function() {
        var _this = this;
        if (this.running_loop) {
            if (!this.pause_processing) {
                this.processMessage();
            }
            setTimeout(
                function() {
                    _this.loopProcessMessage();  
                },
                50
            );
        }    
    };
    
    GameTexasPokerClient.prototype.startLoop = function() {
        this.running_loop = true;
        this.loopProcessMessage();    
    };
    
    GameTexasPokerClient.prototype.stopLoop = function() {
        this.running_loop = false;
    };
    
    
    GameTexasPokerClient.prototype.joinRoom = function () {
        var betting_money = 100;
        var join_command = {command: "join", arguments: {"betting_money": betting_money}};
        sendCommand(join_command);
        this.startLoop();
        //this.playScene();
    };
    
    GameTexasPokerClient.prototype.partRoom = function () {
        this.game = null;
        var part_command = {command: "part", arguments: []};
        sendCommand(part_command);
        this.startScene();        
        //this.stopLoop();
    };
    
    GameTexasPokerClient.prototype.readyRoom = function () {
        var ready_command = {command: "ready", arguments: []};
        sendCommand(ready_command);            
    };
    
    GameTexasPokerClient.prototype.logOut = function () {
        CocoonJS.App.forwardAsync("logOutSession();", function(){});
        this.loginFailed = true;
        this.userinfo = null;
        this.game = null;
    };

    GameTexasPokerClient.prototype.processJoin = function (message) {
        var player = message["player"];
        if (player["username"] == this.userinfo.userid) {
            /*you've just joined a room*/
           //this.pause_processing = true;           
           this.playScene();
        }
        else {
            //draw other player go in your room
        }
    };
    
    GameTexasPokerClient.prototype.processPart = function (message) {
        var player = message["player"];
        if (player == this.userinfo.userid) {
            /*you've just parted a room*/
        	if (this.game) {
        		this.game.sounds.lose.play();
        	}
        	this.startScene();
        }
        else {
        	if (this.game) {
        		this.game.sounds.win.play();
        	}
        }
    };
    
    GameTexasPokerClient.prototype.processStartGame = function(message) {
        var _this = this;
        this.default_stake = message["betting_money"];
        this.pause_processing = true;
        this.my_pot = 0;
        this.enemy_pot = 0;
        this.current_round = 0;
        var wait_for_game = function() {
            if (_this.game) {
                _this.game.startGame();
                _this.game.default_stake = _this.default_stake;
                //_this.pause_processing = false;
                console.log('STARTGAME');
            }
            else {
                setTimeout(function() {
                    wait_for_game();    
                }, 100);
            }
        };
        wait_for_game();        
    };
    
    GameTexasPokerClient.prototype.processBet = function (message) {
        var player = message["player"];
        var action = message["action"];
        var amount = message["amount"];
        if (action == "big_blind") {
            this.big_blind = player;
            this.big_blind_amount = amount;
            if (this.big_blind == this.userinfo.userid) {
                this.game.drawBigBlind("down");
            }
            else {
                this.game.drawBigBlind("up");
            }            
        }
        if (action == "small_blind") {
            this.small_blind = player;
        }
        if (player == this.userinfo.userid) {            
            if (action == "big_blind" || action =="small_blind") {
                this.my_pot = 0;
            }
            this.my_pot += amount;
        }
        else {
            if (action == "big_blind" || action =="small_blind") {
                this.enemy_pot = 0;
            }
            this.enemy_pot += amount;
        }
        this.game.up_pot.value = this.enemy_pot;
        this.game.down_pot.value = this.my_pot;
        
        if (action == "check") {
        	if (this.game) {
        		this.game.sounds.check.play();
        	}
        }
        
        if (action == "call" || action == "raise") {
        	if (this.game) {
        		this.game.sounds.call.play();
        	}
        }
    };
    
    GameTexasPokerClient.prototype.processFold = function (message) {
        var player = message["player"];
        if (this.game) {
    		this.game.sounds.showdown.play();
    		if (this.userinfo.userid != player) {
            	this.game.sounds.win.play();
            }
            else {
            	this.game.sounds.lose.play();
            }
    		this._pauseProcessing(1);
    	}
    };
    
    GameTexasPokerClient.prototype.processTurn = function (message) {
        var player = message["player"];
        if (player == this.userinfo.userid) {
            this.game.drawTimeBar("down");
        }
        else {
            this.game.drawTimeBar("up");
        }
    };
    
    GameTexasPokerClient.prototype.processStake = function (message) {
        var player = message["player"];
        var stake = Number(message["stake"]);
        console.log(["Stake", stake]);
        if (player == this.userinfo.userid) {
            if (this.game) {
                this.game.setHP("down", stake);                
            }
            this.my_stake = stake;                        
        }
        else {
            if (this.game) {
                this.game.setHP("up", stake);                
            }
            this.enemy_stake = stake;
        }
    };
    
    GameTexasPokerClient.prototype.processDealCommunity = function(message) {
        this.current_round +=1;
        var cards = message["cards"];
        this._pauseProcessing(1);
        if (this.current_round == 1) {
            this.game.drawFlop(cards);
        }
        else if (this.current_round == 2) {
            this.game.drawTurn(cards[0]);
        }
        else if (this.current_round == 3) {
            this.game.drawRiver(cards[0]);
        }
    };
    
    GameTexasPokerClient.prototype.processSubmit = function(message) {
        this.current_round +=1;
        var player = message["player"];
        var cards = message["cards"];
        if (player != this.userinfo.userid) {
            this.game.drawShowDown(cards);
        }
    };
    
    GameTexasPokerClient.prototype.processStopGame = function() {
        if (this.game) {
            if (this.current_round == 4) {
                this._pauseProcessing(3);
            }            
        }
    };
    
    GameTexasPokerClient.prototype.processStopMatch = function() {
        if (this.game) {
            this.game.clearGame();
            this.game.waiting = true;
            this.game.drawConfirmDialog();            
        }
    };
    
    GameTexasPokerClient.prototype.processDeal = function(message) {
        if (this.game) {
            this.game.clearCards();
        }
        var cards = message["card_set"];
        this.game.drawPreFlop(cards);
        this.current_round = 0;
    };
    
    GameTexasPokerClient.prototype.processWinner = function(message) {
        var cards = message["cards"];
        var player = message["player"];
        if (this.game) {
            this.game.highlightCards(cards);
            if (this.userinfo.userid == player) {
            	this.game.sounds.win.play();
            }
            else {
            	this.game.sounds.lose.play();
            }
            this._pauseProcessing(5);         
        }
    };
        
    GameTexasPokerClient.prototype.bet_fold = function() {
        var command = {"command": "bet", "arguments":{"action": "fold"}};
        sendCommand(command);    
    };
    
    GameTexasPokerClient.prototype.bet_call_or_check = function() {
        var diff = this.enemy_pot - this.my_pot;
        var command = {};
        if (diff == 0) {
            command = {"command": "bet", "arguments": {"action": "check"}};
        }
        else if (diff > 0) {
            command = {"command": "bet", "arguments": {"action": "call", "amount": Math.min(diff, this.my_stake)}};
        }
        sendCommand(command);    
    };
    
    GameTexasPokerClient.prototype.bet_raise = function() {
        var current_bet = Math.max(this.my_pot, this.enemy_pot);
        var required_bet_amount = 0;
        if (this.current_round <= 1) {
            required_bet_amount = this.big_blind_amount;
        }
        else {
            required_bet_amount = this.big_blind_amount * 2;
        }
        var new_bet = current_bet + required_bet_amount;
        var amount = new_bet - this.my_pot;
        var command = {"command": "bet", 
                    "arguments":{"action": "raise", "amount": amount}};
        console.log(command);
        sendCommand(command);
    };
    
    GameTexasPokerClient.prototype._pauseProcessing = function(seconds) {
        this.pause_processing = true;
        var _this = this;
        setTimeout(function() {
            _this.pause_processing = false;                
        }, seconds * 1000);          
    };
    
    return GameTexasPokerClient;
}
);