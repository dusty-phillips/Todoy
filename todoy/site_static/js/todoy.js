var setup_main_page = function() {
    var __kwargs = __kwargs_get(arguments);
    var __varargs = __varargs_get(arguments);
    var $v1 = Array.prototype.slice.call(arguments).concat(js(__varargs));
    jQuery("#add_form").submit(submit_add_form);
    window.setInterval(check_online, 5000);
return None;
}
var check_online = function() {
    var __kwargs = __kwargs_get(arguments);
    var __varargs = __varargs_get(arguments);
    var $v2 = Array.prototype.slice.call(arguments).concat(js(__varargs));
    if (bool(navigator.onLine) === True) {
        jQuery("#online_indicator").html("ONLINE");
    } else {
        jQuery("#online_indicator").html("OFFLINE");
    }
return None;
}
var submit_add_form = function() {
    var __kwargs = __kwargs_get(arguments);
    var __varargs = __varargs_get(arguments);
    var $v3 = Array.prototype.slice.call(arguments).concat(js(__varargs));
    var ev = ('ev' in __kwargs) ? __kwargs['ev'] : $v3[0];
    delete __kwargs.ev
    alert("submitted");
    return js(False);
}

