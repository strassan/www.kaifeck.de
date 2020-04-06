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

  // Load in YouTube videos from php/data/youtube_uploads.json
  $.ajax({
    url: "php/data/youtube_uploads.json",
    success: function (data) {
      for (let i = 0; i <= 5; i++) {
        $('#songFrame' + (i+1).toString()).html('<iframe class="embed-responsive-item mb-3 mb-lg-0" src="https://www.youtube.com/embed/' + data[i].href + '" allowfullscreen></iframe>');
        $('#songTitle' + (i+1).toString()).html(data[i].title);
      }
    }
  });


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
    // make all messages invisible
    $("#successMsgSent").addClass("d-none");
    $("#errorMsgEmail").addClass("d-none");
    $("#errorMsgFail").addClass("d-none");
    $("#errorMsgText").addClass("d-none");
    $("#errorMsgPear").addClass("d-none");

    // check if the text is empty
    var is_message_empty = true;
    var message = $.trim($("#messageInput").val());
    if (message == "") {
      $("#errorMsgText").removeClass("d-none");
    }
    else {
      is_message_empty = false;
    }

    // check validity of email
    var email_address = $.trim($("#emailInput").val());
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    var is_email_valid = regex.test(email_address);
    if (!is_email_valid) {
      $("#errorMsgEmail").removeClass("d-none");
    }

    // send email via post
    if (!is_message_empty && is_email_valid) {
      var email = $("#emailInput").val();
      var text = $("#messageInput").val();
      $("#waitMsg").removeClass("d-none");
      $.ajax({
        type: "POST",
        url: "php/send_mail.php",
        data: {
          email: email,
          text: text
        },
        success: function (data, status) {
          $("#waitMsg").addClass("d-none");
          if (data.localeCompare("success") == 0) {
            $("#successMsgSent").removeClass("d-none");
            $("#messageInput").val('');
            $("#emailInput").val('');
          } else if (data.localeCompare("fail") == 0) {
            $("#errorMsgFail").removeClass("d-none");
          } else {
            $("#errorMsgPear").removeClass("d-none");
            $("#errorMsgPear").html(data);
          }
        }
      });
    }
    else {
      $("#successMsgSent").addClass("d-none");
    }
  });

})(jQuery); // End of use strict
