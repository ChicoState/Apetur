setInterval(function () {
    var new_image_url = $('.next-image img').data('image-url');
    var cur_image = $('.featuring-image');
    cur_image.fadeOut('fast', function () {
        cur_image.attr('src', new_image_url)
            .fadeIn('fast');
    })

    $('.featured-queue-item').each(function () {
        if ($(this).hasClass('next-image')) {
            $(this).css('order', $('.featured-queue-item').length)
                .removeClass('next-image');
        } else {
            var newOrder = parseInt($(this).css('order')) - 1;
            if (newOrder == 1) {
                $(this).addClass('next-image');
            }
            $(this).css({
                order: newOrder
            });
        }
    });
}, 5000);