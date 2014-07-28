define([], function() {
    return {
        get: function() {
            var json_value = localStorage['session'];
            if (json_value) {
                return JSON.parse(json_value);
            }
            return null;    
        },
        set: function(value_object) {
            var json_value = JSON.stringify(value_object);
            localStorage['session'] = json_value;
        },
        clear: function() {
            localStorage.removeItem('session');
        },    
    };    
});
