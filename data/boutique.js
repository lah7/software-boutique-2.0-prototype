
/************************
 * Global
************************/
// Commands → Python
function cmd(instruction) {
    document.title = instruction;
    setTimeout(function(){
        document.title = 'null';
    }, 10);
}

// Scroll to top of page
function backToTop() {
    $('#content').animate({
        scrollTop: 0
    }, 600);
    $('#scroll-top').addClass('active');
    return false;
};

// Smoothly fade between two elements (by ID)
function smoothFade(from, to, speed) {
    if ( speed == 'fast' ) {
        speed_val = 300;
    } else if ( speed == 'faster' ) {
        speed_val = 150;
    } else if ( speed == 'medium' ) {
        speed_val = 500;
    } else if ( speed == 'slow' ) {
        speed_val = 1000;
    } else {
        speed_val = 500;
    }
    $(from).fadeOut(speed_val);
    setTimeout(function() {
        $(to).fadeIn(speed_val);
    }, speed_val);
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

function animate(element, ani_class, direction) {
    $(element).addClass(ani_class);
    setTimeout(function() {
        $(element).removeClass(ani_class);
    }, 600)

    if ( direction == 'in' ) {
        $(element).fadeIn(500);
    }

    if ( direction == 'out' ) {
        $(element).fadeOut(500);
    }
}

/************************
 * Events
************************/
// Page finished loading
$(document).ready(function() {

    // Show back to top button on page scroll
    $('#content').scroll(function () {
        if ($(this).scrollTop() > 90) {
          $('#scroll-top').removeClass('disabled');
        } else {
          $('#scroll-top').addClass('disabled');
        }
    });
});

/************************
 * First Run Introduction
************************/
firstRunLastNo = 0;
firstRunCurrentNo = 1;
firstRunMaxNo = 3;

function firstRunUpdatePage() {
    if ( firstRunCurrentNo == 1 ) {
        $('#firstrun-prev').addClass('disabled');
    } else {
        $('#firstrun-prev').removeClass('disabled');
    }

    if ( firstRunCurrentNo == firstRunMaxNo ) {
        $('#firstrun-next').hide();
        $('#firstrun-start').show();
        $('#firstrun-skip').addClass('disabled');
    } else {
        $('#firstrun-next').show();
        $('#firstrun-start').hide();
        $('#firstrun-skip').removeClass('disabled');
    }

    $('.blob').removeClass('done');
    $('#firstrun-blob-'+firstRunCurrentNo).addClass('done');
}

function firstRunNextPage() {
    if ( firstRunCurrentNo + 1 > firstRunMaxNo ) {
        return
    }

    firstRunLastNo = firstRunCurrentNo;
    firstRunCurrentNo = firstRunCurrentNo + 1;

    animate('#firstrun-page'+firstRunLastNo, 'left-out', 'out');
    animate('#firstrun-page'+firstRunCurrentNo, 'left-in', 'in');
    firstRunUpdatePage();
}

function firstRunPrevPage() {
    if ( firstRunCurrentNo - 1 < 1 ) {
        return
    }

    firstRunLastNo = firstRunCurrentNo;
    firstRunCurrentNo = firstRunLastNo - 1;

    animate('#firstrun-page'+firstRunLastNo, 'right-out', 'out');
    animate('#firstrun-page'+firstRunCurrentNo, 'right-in', 'in');
    firstRunUpdatePage();
}

function firstRunDismiss() {
    cmd('first-run-complete');
}

/************************
 * Menus
************************/
function categoryOpen() {
    smoothFade('#change-category-button', '#change-category-button-close', 'faster');
    $('#categories-page').slideDown();
    $('#categories-page').scrollTop(0);
}

function categoryClose() {
    smoothFade('#change-category-button-close', '#change-category-button', 'faster');
    $('#categories-page').slideUp();
}

function changeCategory(internal_name, human_name) {
    $('#current-category-icon').attr('src', 'categories/' + internal_name + '.svg');
    $('#current-category-text').html(human_name);
    categoryClose();
    smoothFade('.category-contents', '#category-' + internal_name, 'fast');
    $('#backdrop-icon').fadeOut();
    setTimeout(function() {
        $('#backdrop-icon').attr('src', 'categories/' + internal_name + '.svg');
        $('#backdrop-icon').fadeIn();
    }, 300);
}
