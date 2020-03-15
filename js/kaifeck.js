(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 70)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 100
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-shrink");
    } else {
      $("#mainNav").removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Change "Show more" button text on collapse
  $('#collapse-songs').on('shown.bs.collapse', function () {
    $('#btn-show-songs').html('Show less')
  });
  // Change "Show less" button text on hide
  $('#collapse-songs').on('hidden.bs.collapse', function () {
    $('#btn-show-songs').html('Show More')
  });
  // Scroll up when collapsing
  $('#collapse-songs').on('hide.bs.collapse', function () {
    $([document.documentElement, document.body]).animate({
      scrollTop: $("#collapse-songs").offset().top - 500
    }, 500);

  });

  // Functionality of the "send" button for emails
  $('#btn-send-mail').click(function () {
    // check if the text is empty
    var is_message_empty = true;
    var message = $.trim($("#messageInput").val());
    if (message == "") {
      $("#errorMsgText").removeClass("d-none");
    }
    else {
      $("#errorMsgText").addClass("d-none");
      is_message_empty = false;
    }

    var email_address = $.trim($("#emailInput").val());
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    var is_email_valid = regex.test(email_address);
    if (!is_email_valid) {
      $("#errorMsgEmail").removeClass("d-none");
    }
    else {
      $("#errorMsgEmail").addClass("d-none");
    }

    if (!is_message_empty && is_email_valid) {
      $('#emailForm').submit();
      $("#successMsgSent").removeClass("d-none");
      $("#messageInput").val('');
      $("#emailInput").val('');
    }
    else {
      $("#successMsgSent").addClass("d-none");
    }
  });

})(jQuery); // End of use strict
