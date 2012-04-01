var setup = function() {
    var __kwargs = __kwargs_get(arguments);
    var __varargs = __varargs_get(arguments);
    var $v1 = Array.prototype.slice.call(arguments).concat(js(__varargs));
    validate(str('#registration_form'), dict([str('confirm_password'), str('The passwords do not match')]), __kwargs_make({username: str('required'), password: str('required'), confirm_password: dict([str('equalTo'), str('input[name=password]')])}));
return None;
}
var validate = function() {
    var kwargs = __kwargs_get(arguments);
    var __varargs = __varargs_get(arguments);
    var $v2 = Array.prototype.slice.call(arguments).concat(js(__varargs));
    var selector = ('selector' in kwargs) ? kwargs['selector'] : $v2[0];
    delete kwargs.selector
    if (selector === undefined) { 
__builtins__.PY$print('validate() did not get parameter selector'); }; 
    var mess = $v2[1];
    if (mess === undefined) { mess = kwargs.mess === undefined ? __builtins__.PY$None : kwargs.mess; };
    delete kwargs.mess
    if (mess === undefined) { 
__builtins__.PY$print('validate() did not get parameter mess'); }; 
    kwargs = dict(kwargs);
    if (bool(mess.PY$__eq__(__builtins__.PY$None)) === True) {
        mess = dict([]);
    }
    jQuery(js(selector)).validate({"rules": js(kwargs), "messages": js(mess)});
return None;
}
jQuery(js(setup));

