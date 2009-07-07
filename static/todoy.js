
function setup_gears() {
    if (!window.google || !google.gears) {
        location.href = "http://gears.google.com/?action=install&message=gears+is+required+to+use+todoy" +
        "&return=http://todoy.archlinux.ca/todoy/";
    }
    var localServer = google.gears.factory.create('beta.localserver');
    var store = localServer.createManagedStore('test-store');
    store.manifestUrl = '/static/todoy_manifest.json';
    store.checkForUpdate();
}
