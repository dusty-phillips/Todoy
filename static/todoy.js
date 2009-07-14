
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
    db = db_connection();
    var todo_date = $.url.param('todo_date');
    if (!todo_date) {
        todo_date = new Date().toDBDate();
    }
    $('#date_header').html(todo_date);
    $('#todo_date').datepicker({dateFormat: 'yy-mm-dd'});
    $('#todo_time').timepickr({convention: '12'});
    $('.complete_todo').live('click', complete_todo);
    var rs = db.execute(
        "select local_id, title, time, completed from todos where date=?",
            [todo_date]);
    while (rs.isValidRow()) {
        todo = {
            'local_id': rs.fieldByName('local_id'),
            'title': rs.fieldByName('title'),
            'completed': rs.fieldByName('completed'),
            'time': rs.fieldByName('time')
        }
        $('#day_list').append(render_todo_item(todo));
        rs.next();
    }
}

function switch_day(increment) {
    var target_date = param_date_or_today();
    target_date.setDate(target_date.getDate() + increment);
    redirect('/todos/?todo_date=' + target_date.toDBDate());
}

function add_todo() {
    clear_todo_form();
    $('#todo_date').val(param_date_or_today().toDBDate());
    $('#save_button').click(save_new_todo);
    $('#close_button').click(function () {$('#todo_edit_box').fadeOut();});
    $('#todo_id').val("NEW");
    $('#todo_edit_box').fadeIn();
}

function complete_todo(evt) {
    var re = /todo-item-(\d+)/;
    var id = $(this).parent().attr('id');
    id = id.match(re)[1];
    db = db_connection();
    db.execute("update todos set completed = 'true' where local_id = ?",
            [id]);
    $(this).parent().attr('class', 'completed');

}

function clear_todo_form() {
    $('#todo_date').val('');
    $('#todo_title').val('');
    $('#todo_time').val('');
}

function save_new_todo() {
    db = db_connection();
    var todo = {
        'modified': new Date().toISOString(),
        'time': $('#todo_time').val(),
        'date': $('#todo_date').val(),
        'title': $('#todo_title').val()
    }
    db.execute(
            'insert into todos ' +
            '(modified, date, time, title) values ' +
            '(?, ?, ?, ?)',
            [todo.modified,
            todo.date,
            todo.time,
            todo.title
            ]);
    rs = db.execute('select last_insert_rowid()');
    todo.local_id = rs.field(0);
    window.location.reload(true);
}

function render_todo_item(todo) {
    var li = "<li id = 'todo-item-" + todo.local_id;
    if (todo.completed == 'true') {
        li = li + "' class='completed";
    }
    li = li + "'><span class='complete_todo'>" + todo.title + "</span></li>";
    return li;
}

//UTILITY FUNCTIONS
function db_connection() {
    db = google.gears.factory.create('beta.database');
    db.open('todoy-database');
    db.execute('create table if not exists todos' +
            ' (local_id integer PRIMARY KEY AUTOINCREMENT,' +
            ' server_id varchar null,' +
            ' date date,' +
            ' time time default \'\',' +
            ' title varchar default \'\',' +
            ' modified datetime,' +
            ' deleted boolean default false,' +
            ' completed boolean default false' +
            ')'
            );
    return db;
}

function pad_zero(digit) {
    // return a string that is at least two digits long
    var retstr = '' + digit;
    if (retstr.length < 2) {
        return '0' + retstr;
    }
    return retstr;
}

function redirect(path) {
    window.location.href = window.location.protocol +
       '//' + window.location.host + path;
}

function param_date_or_today() {
    var target_date = new Date();
    var todo_date = $.url.param('todo_date');
    if (todo_date) {
        target_date.fromDBDate(todo_date);
    }
    return target_date;
}

Date.prototype.toDBDate = function () {
    return this.getFullYear() + '-' + pad_zero(this.getMonth()+1) + '-' +
        pad_zero(this.getDate());
}

Date.prototype.fromDBDate = function(string) {
    var regexp = "([0-9]{4})-([0-9]{2})-([0-9]{2})";
    var d = string.match(new RegExp(regexp));
    this.setFullYear(d[1]);
    this.setMonth(d[2] - 1);
    this.setDate(d[3]);
}

Date.prototype.toDBDatetime = function () {
    return this.toDBDate() + 'T' + pad_zero(this.getHours()) + ':' +
            pad_zero(this.getMinutes()) + ':' + pad_zero(this.getSeconds());
}


Date.prototype.toISOString = function (format, offset) {
    /* accepted values for the format [1-6]:
     1 Year:
       YYYY (eg 1997)
     2 Year and month:
       YYYY-MM (eg 1997-07)
     3 Complete date:
       YYYY-MM-DD (eg 1997-07-16)
     4 Complete date plus hours and minutes:
       YYYY-MM-DDThh:mmTZD (eg 1997-07-16T19:20+01:00)
     5 Complete date plus hours, minutes and seconds:
       YYYY-MM-DDThh:mm:ssTZD (eg 1997-07-16T19:20:30+01:00)
     6 Complete date plus hours, minutes, seconds and a decimal
       fraction of a second
       YYYY-MM-DDThh:mm:ss.sTZD (eg 1997-07-16T19:20:30.45+01:00)
    */
    if (!format) { var format = 6; }
    if (!offset) {
        var offset = 'Z';
        var date = this;
    } else {
        var d = offset.match(/([-+])([0-9]{2}):([0-9]{2})/);
        var offsetnum = (Number(d[2]) * 60) + Number(d[3]);
        offsetnum *= ((d[1] == '-') ? -1 : 1);
        var date = new Date(Number(Number(this) + (offsetnum * 60000)));
    }

    var zeropad = function (num) { return ((num < 10) ? '0' : '') + num; }

    var str = "";
    str += date.getUTCFullYear();
    if (format > 1) { str += "-" + zeropad(date.getUTCMonth() + 1); }
    if (format > 2) { str += "-" + zeropad(date.getUTCDate()); }
    if (format > 3) {
        str += "T" + zeropad(date.getUTCHours()) +
               ":" + zeropad(date.getUTCMinutes());
    }
    if (format > 5) {
        var secs = Number(date.getUTCSeconds() + "." +
                   ((date.getUTCMilliseconds() < 100) ? '0' : '') +
                   zeropad(date.getUTCMilliseconds()));
        str += ":" + zeropad(secs);
    } else if (format > 4) { str += ":" + zeropad(date.getUTCSeconds()); }

    if (format > 3) { str += offset; }
    return str;
}

Date.prototype.setISO = function (string) {
    var regexp = "([0-9]{4})(-([0-9]{2})(-([0-9]{2})" +
        "(T([0-9]{2}):([0-9]{2})(:([0-9]{2})(\.([0-9]+))?)?" +
        "(Z|(([-+])([0-9]{2}):([0-9]{2})))?)?)?)?";
    var d = string.match(new RegExp(regexp));

    var offset = 0;
    var date = new Date(d[1], 0, 1);

    if (d[3]) { date.setMonth(d[3] - 1); }
    if (d[5]) { date.setDate(d[5]); }
    if (d[7]) { date.setHours(d[7]); }
    if (d[8]) { date.setMinutes(d[8]); }
    if (d[10]) { date.setSeconds(d[10]); }
    if (d[12]) { date.setMilliseconds(Number("0." + d[12]) * 1000); }
    if (d[14]) {
        offset = (Number(d[16]) * 60) + Number(d[17]);
        offset *= ((d[15] == '-') ? 1 : -1);
    }

    offset -= date.getTimezoneOffset();
    time = (Number(date) + (offset * 60 * 1000));
    this.setTime(Number(time));
}
