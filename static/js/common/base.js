/*
 * Navbar Scroll Transition - START
 ********************************************/
$nav_show = false;
$navbar_selector = $('.navbar-container');
$have_transparent_nav = $navbar_selector.is('.navstyle-fixed, .navstyle-sticky') && !$navbar_selector.hasClass('.no-transition');

$(document).scroll(function () {
    if ($have_transparent_nav) {
        // navbar background transition when scroll pass fetured section
        $scrollHeight = $navbar_selector.height();

        if ($(document).scrollTop() > $scrollHeight && !$nav_show) {
            $navbar_selector.addClass('show-color');
            $nav_show = true;
        } else if ($(document).scrollTop() < $scrollHeight && $nav_show) {
            $navbar_selector.removeClass('show-color');
            $nav_show = false;
        }
    }
});
/*
 * Navbar Scroll Transition - END
 ********************************************/

// Add slideDown animation to Bootstrap dropdown when expanding.
$('.dropdown').on('show.bs.dropdown', function (e) {
    var dropdown_menu = $(this).find('.dropdown-menu').first();
    if (dropdown_menu.hasClass('slide')) {
        dropdown_menu.stop(true, true).animate({
            right: '0'
        }, 250);
    } else {
        dropdown_menu.stop(true, true).slideDown(250);
    }
});

// Add slideUp animation to Bootstrap dropdown when collapsing.
$('.dropdown').on('hide.bs.dropdown', function () {
    var dropdown_menu = $(this).find('.dropdown-menu').first();
    if (dropdown_menu.hasClass('slide')) {
        dropdown_menu.stop(true, true).animate({
            right: '-' + dropdown_menu.css('width')
        }, 250);
    } else {
        dropdown_menu.stop(true, true).slideUp(250);
    }
});