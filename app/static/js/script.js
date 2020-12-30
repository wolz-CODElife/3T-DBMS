// script for pre-loader
$(document).ready(function() {
  setTimeout(function(){
    var loaderTimeout = 3000;
    $('#loader').fadeOut();
    $('#content').fadeIn(loaderTimeout);
  }, 1000);
  $('#hambuger').click(function () {
    $("#nav").toggle();
  });

  // Select all checkbox on constomer page
  $('#selectall').click(function(){
    if($('#selectable #selectall').is(':checked')){
      $('#selectable input[type=checkbox]').each(function(){
        $(this).prop("checked", true);
      });
    }
    else{
      $('#selectable input[type=checkbox]').each(function(){
        $(this).prop("checked", false);
      });
    }
  });
});

