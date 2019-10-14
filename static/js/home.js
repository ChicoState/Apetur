$nav_show = false;

$('.navbar-toggler').click(function () {
    if ($('#navbarNav').hasClass('show')) {
        // $('.navbar').css('background', '');
        $('.navbar').removeClass('show-color');

    } else {
        // $('.navbar').css('background', '#7C7C7C');
        $('.navbar').addClass('show-color');

    }
});

$(document).scroll(function () {
    // navbar background transition when scroll pass fetured section
    $scrollHeight = $('.navbar').height();

    if ($(document).scrollTop() > $scrollHeight && !$nav_show) {
        $('.navbar').addClass('show-color');
        $nav_show = true;
    } else if ($(document).scrollTop() < $scrollHeight && $nav_show) {
        $('.navbar').removeClass('show-color');
        $nav_show = false;
    }
});

// Add slideDown animation to Bootstrap dropdown when expanding.
$('.dropdown').on('show.bs.dropdown', function () {
    $(this).find('.dropdown-menu').first().stop(true, true).slideDown(250);
});

// Add slideUp animation to Bootstrap dropdown when collapsing.
$('.dropdown').on('hide.bs.dropdown', function () {
    $(this).find('.dropdown-menu').first().stop(true, true).slideUp(250);
});