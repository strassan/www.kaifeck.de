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
    let logo = document.getElementById('logo');
    if (mainNav.offset().top > 100) {
      mainNav.addClass("navbar-shrink");
      logo.src = "/static/website/img/logo/logo_black.svg";
      logo.style = "opacity: 1;";
    } else {
      mainNav.removeClass("navbar-shrink");
      if (window.matchMedia("(min-width: 992px)").matches) {
        logo.src = "/static/website/img/logo/logo_white.svg";
        logo.style = "opacity: 0.6;";
      }
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

})(jQuery); // End of use strict
