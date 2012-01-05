@JSVar("jQuery", "window")
def setup_main_page():
    jQuery('#add_form').submit(submit_add_form)
    window.setInterval(check_online, 5000)

@JSVar('jQuery', 'navigator')
def check_online():
    if navigator.onLine:
        jQuery('#online_indicator').html("ONLINE")
    else:
        jQuery('#online_indicator').html("OFFLINE")


@JSVar("alert")
def submit_add_form(ev):
    alert('submitted')
    return js(False)

#jQuery(document).delegate("#main_page", "pagecreate", setup_main_page)
