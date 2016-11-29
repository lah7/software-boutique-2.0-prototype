// Pass commands to Python
function cmd(instruction) {
    document.title = instruction;
    setTimeout(function(){
        document.title = 'null';
    }, 10);
}

// Global across all pages
$(window).load(function() {
    // Smoothly fade into the page.
    $('.entire-page-fade').jAnimate('pageIn');
    $('.entire-page-fade').show();
    $('#navigation-right').hide();
    $('#navigation-right').fadeIn('medium');
});

// Back to the top function
function backToTop() {
    $("#content").animate({
        scrollTop: 0
    }, 600);
    $('#scroll-top').addClass('active');
    return false;
};

// When page first opens
$(document).ready(function() {
  // Animate navigation elements on page load
  if ( current_page != 'splash-boutique.html' ) {
    if ( current_page != 'software.html') {
      $('#menu-button').show();
      $('#menu-button').jAnimateOnce('pageIn');
      $('#navigation-title').show();
      $('#navigation-title').jAnimateOnce('pageIn');
    }
  }

  // Show back to top button on page scroll
  $('#content').scroll(function () {
      if ($(this).scrollTop() > 90) {
          $('#scroll-top').fadeIn();
          $('#scroll-top-always-show').removeClass('disabled');
      } else {
          $('#scroll-top').fadeOut();
          $('#scroll-top').removeClass('active');
          $('#scroll-top-always-show').addClass('disabled');
      }
  });
});

// Smoothly fade between two elements (by ID)
function smoothFade(from, to) {
  $(from).fadeOut();
  setTimeout(function(){ $(to).fadeIn(); }, 400 );
}

// Smoothly fade the navigation sub-title
function changeSubtitle(textToDisplay) {
  // Smoothly fade subtitle
  $('#navigation-sub-title').fadeOut('fast');
  setTimeout(function() {
    $('#navigation-sub-title').html(textToDisplay);
    $('#navigation-sub-title').fadeIn('fast');
  }, 200);
}

// For pages that depend on an internet connection, but we couldn't connect.
function reconnectRetry() {
  cmd('checkInternetConnection');
  if ( ! $('#reconnectFailed').is(':visible') ) {
    $('#reconnectFailed').fadeIn();
  } else {
    $('#reconnectFailed').jAnimateOnce('flash');
  }
}

// Dynamically set the cursor,
function setCursorBusy() {
  $('html').addClass('cursor-wait');
  $('body').addClass('cursor-wait');
  $('a').addClass('cursor-wait');
}

function setCursorNormal() {
  $('html').removeClass('cursor-wait');
  $('body').removeClass('cursor-wait');
  $('a').removeClass('cursor-wait');
}

