require.config({
    urlArgs: "bust=" + (new Date()).getTime(),
});

require([
         "webview/publicscript",
         "webview/utils",
         "vendor/cocoon"
         ], 
         function() 
{
    //do nothing
});
