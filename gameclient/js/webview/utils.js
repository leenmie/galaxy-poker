function showUp(leftCorner_x, leftCorner_y, screen_width, screen_height, percent, content) {                   
        var width = 0;
        var height = 0;
        if (width == 0) {
            
            width = screen_width;
            height = screen_height;
        }

        var left_corner_x = leftCorner_x;
        var left_corner_y = leftCorner_y;
        if (percent) {
            width = width * percent;
            height = height * percent;
        }        
        CocoonJS.App.show(left_corner_x, left_corner_y, width, height);
        CocoonJS.App.disableTouchInCocoonJS();
        if (content) {
            af.ui.loadContent(content);
        }
}

function hideOut() {
    CocoonJS.App.enableTouchInCocoonJS();
    CocoonJS.App.hide();
    af.ui.hideMask();
}
