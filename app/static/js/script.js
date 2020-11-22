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
});
