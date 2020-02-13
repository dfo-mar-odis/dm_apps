  // js script to add date to notes field
  $("#insertDate").click(function() {

    var options = {  year: 'numeric', month: 'short', day: 'numeric' };
    var today = new Date();
    var strDate = today.toLocaleDateString("en-US", options);
    var strInjection = "- `" + strDate + " (" + user_name + ")`: ";

    if ($("#id_notes").val()==="") {
      strInjection = strInjection;
    }else {
      strInjection =  strInjection + "\n";
    }

    $("#id_notes").val(strInjection + $("#id_notes").val())

  })
