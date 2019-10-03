$nav_show = false;

$(document).scroll(function () {
    $scrollHeight = $('#featured').height() - $('.navbar').height();

    if ($(document).scrollTop() > $scrollHeight && !$nav_show) {
        $('.navbar').addClass('show-color');
        $nav_show = true;
    } else if ($(document).scrollTop() < $scrollHeight && $nav_show) {
        $('.navbar').removeClass('show-color');
        $nav_show = false;
    }
});