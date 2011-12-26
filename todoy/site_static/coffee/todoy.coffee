setup_main_page = ->
  $('#add_form').submit(submit_add_form)

submit_add_form = (ev) ->
  alert 'submitted'
  return false

$(document).delegate "#main_page", "pagecreate", setup_main_page
