// Used jquery v3.5.1 and font-awesome v4.7.0
$(document).ready(function() {
    $('.nav .dropdown-menu').prev('a').on('click', function(e) {
      e.preventDefault();
      $(this).parent().find('.dropdown-menu').slideToggle();
    });
});