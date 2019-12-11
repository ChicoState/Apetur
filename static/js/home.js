// when progress bar finished with its animation
$('.progress-end').on('animationend webkitAnimationEnd oAnimationEnd MSAnimationEnd',
    function () {
        featureRotation('next');
        var parent_progress = $(this).closest('.progress');

        // restart the animation
        var right_progress_bar = parent_progress.find('.progress-right .progress-bar');
        right_progress_bar.removeClass('progress-bar');

        var left_progress_bar = parent_progress.find('.progress-left .progress-bar');
        left_progress_bar.removeClass('progress-bar');

        setTimeout(function () {
            right_progress_bar.addClass('progress-bar');
            left_progress_bar.addClass('progress-bar');
        }, 1);
    }
);

// pause the animation when hover over the progress circle
$('.progress').mouseenter(function () {
    $('.progress').addClass('pause-animation');
})

// resume the animation when mouse leave the progress circle
$('.progress').mouseleave(function () {
    $('.progress').removeClass('pause-animation');
})

/**
 * The last element in the list of .featured-queue-item will be currently featured
 */
function featureRotation(direction = 'next') {
    var current_feature_order = $('.featured-queue-item').length;

    $('.current-feature').removeClass('current-feature');

    $('.featured-queue-item').each(function () {
        var this_order = parseInt($(this).css('order'));

        // calculating the new order
        if (direction == 'next') {
            this_order--;
            this_order = this_order <= 0 ? current_feature_order : this_order;
        } else {
            this_order++;
            this_order = this_order > current_feature_order ? 1 : this_order;
        }
        $(this).css('order', this_order);

        if (this_order == 1) {
            $(this).addClass('current-feature');
        }
    });

    // updating the image
    var cur_image = $('.featuring-image');
    cur_image.fadeOut('fast', function () {
        cur_image.attr('src', $('.current-feature img').data('image-url'))
            .fadeIn('fast');

        // updating profile related datas
        $('.user-detail .featured-user-pic img').attr('src', $('.current-feature img').data('photographer-pic'));
        $('.user-detail .featured-user-name').text($('.current-feature img').data('photographer-name'));
    });

    // upating the circle control
    $('.current-circle-control').removeClass('current-circle-control');
    $('.feature-control-circle').eq($('.current-feature').index())
        .addClass('current-circle-control');
}