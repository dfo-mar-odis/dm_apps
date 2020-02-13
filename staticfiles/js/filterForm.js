// if there is a form called # filter-form, submit the form each time there is a control updated
$("#filter-form").change(function () {
  $(this).submit()
});
