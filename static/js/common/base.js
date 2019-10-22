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
$('.dropdown').on('show.bs.dropdown', function () {
    $(this).find('.dropdown-menu').first().stop(true, true).slideDown(250);
});

// Add slideUp animation to Bootstrap dropdown when collapsing.
$('.dropdown').on('hide.bs.dropdown', function () {
    $(this).find('.dropdown-menu').first().stop(true, true).slideUp(250);
});