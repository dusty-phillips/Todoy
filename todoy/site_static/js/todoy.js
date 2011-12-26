(function() {
  var setup_main_page, submit_add_form;

  setup_main_page = function() {
    return $('#add_form').submit(submit_add_form);
  };

  submit_add_form = function(ev) {
    alert('submitted');
    return false;
  };

  $(document).delegate("#main_page", "pagecreate", setup_main_page);

}).call(this);
