
function setup_gears() {
    if (!window.google || !google.gears) {
        location.href = "http://gears.google.com/?action=install&message=gears+is+required+to+use+todoy" +
        "&return=http://todoy.archlinux.ca/todoy/";
    }
    var localServer = google.gears.factory.create('beta.localserver');
    var store = localServer.createManagedStore('test-store');
    store.manifestUrl = '/static/todoy_manifest.json';
    store.oncomplete = function(details){
        $('#current_version').html("Local Version: " + store.currentVersion);
    };
    store.onerror = function(error){
        alert(error.message);
    }
    store.checkForUpdate();
}

function show_day() {
    setup_gears();
}

function add_todo() {
    $('#save_button').click(save_new_todo);
    $('#close_button').click(function () {$('#todo_edit_box').fadeOut();});
    $('#todo_edit_box').fadeIn();

}
function save_new_todo() {
    alert('saving...');
}

