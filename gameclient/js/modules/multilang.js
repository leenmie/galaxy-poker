define(["i18n!nls/message"], function(message) {
    return {
        getLang: function() {
            return localStorage['locale'];
        },
        setLang: function(lang) {
            localStorage['locale'] = lang;
            requirejs.config({
                config: {
                    //Set the config for the i18n
                    //module ID
                    i18n: {
                        locale: lang,
                    }
                }
            });                                                       
        },
        getDictionary: function() {
            var lang = this.getLang();
            var req2 = require.config({
                context : 'context_' + lang,
                baseUrl : 'js',
                config : {
                    //Set the config for the i18n
                    //module ID
                    i18n : {
                        locale : lang,
                    }
                }
            });
            req2(["require"], function(require) {
                require(["modules/multilang"], function(multilang2) {                    
                                                                                             
                });
            });            
        },
        getMessage: function() {
            return message;  
        },
        apply_language : function(scene) {
            var childrenList = scene.childrenList;
            for (var i in childrenList) {
                if (childrenList[i].text) {
                    var text = childrenList[i].text;
                    console.log(text);                    
                    if (message[text]) {
                        childrenList[i].setText(message[text]);
                    }
                }
                if (childrenList[i].childrenList) {
                    this.apply_language(childrenList[i]);
                }
            }
        },
    };    
});
