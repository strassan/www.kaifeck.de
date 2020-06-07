(function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '')
        && location.hostname === this.hostname) {
      let target = $(this.hash);
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
  let navbarCollapse = function() {
    let mainNav = $("#mainNav");
    if (mainNav.offset().top > 100) {
      mainNav.addClass("navbar-shrink");
    } else {
      mainNav.removeClass("navbar-shrink");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  let collapseSongs = $('#collapse-songs')
  // Change "Show more" button text on collapse
  collapseSongs.on('shown.bs.collapse', function () {
    $('#btn-show-songs').html('Show less')
  });
  // Change "Show less" button text on hide
  collapseSongs.on('hidden.bs.collapse', function () {
    $('#btn-show-songs').html('Show More')
  });
  // Scroll up when collapsing
  collapseSongs.on('hide.bs.collapse', function () {
    $([document.documentElement, document.body]).animate({
      scrollTop: $("#collapse-songs").offset().top - 500
    }, 500);

  });

  // Functionality of the "send" button for emails
  $('#btn-send-mail').click(function () {
    // make all messages invisible
    let waitMsg = $("#waitMsg");
    let successMsg = $("#successMsg");
    let errorMsg = $("#errorMsg");
    waitMsg.addClass("d-none");
    successMsg.addClass("d-none");
    errorMsg.addClass("d-none");
    errorMsg.html("");

    // check if the text is empty
    let is_message_empty = true;
    const message = $.trim($("#messageInput").val());
    if (message === "") {
      errorMsg.removeClass("d-none");
      errorMsg.append("Please enter some text. ");
    }
    else {
      is_message_empty = false;
    }

    // check validity of email
    const email_address = $.trim($("#emailInput").val());
    const regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    let is_email_valid = regex.test(email_address);
    if (!is_email_valid) {
      errorMsg.removeClass("d-none");
      errorMsg.append("Please enter a valid email address. ");
    }

    // get csrf_token
    const csrf_token = $.trim($("input[name=csrfmiddlewaretoken]").val())

    // send email via post
    if (!is_message_empty && is_email_valid) {
      waitMsg.removeClass("d-none");
      $.ajax({
        type: "POST",
        url: "send_mail",
        data: {
          sender_email: email_address,
          sender_message: message,
          csrfmiddlewaretoken: csrf_token
        },
        success: function (data, status) {
          waitMsg.addClass("d-none");
          if (data.localeCompare("success") === 0) {
            successMsg.removeClass("d-none");
            $("#messageInput").val('');
            $("#emailInput").val('');
          } else if (data.localeCompare("fail") === 0) {
            errorMsg.removeClass("d-none");
            errorMsg.append("Oops, something went wrong! ")
          } else {
            errorMsg.removeClass("d-none");
            errorMsg.append("Error " + data);
          }
        }
      });
    }
    else {
      successMsg.addClass("d-none");
    }
  });

})(jQuery); // End of use strict
