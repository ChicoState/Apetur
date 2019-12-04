showLoadingOnLoad();

/*
 * Modal - START
 ********************************************/
var modal = document.getElementById('imagePopupModal');

$('.modal-popup-image').each(function () {
    $(this).click(function () {
        modal.style.display = "block";
        $('#modalImage').attr('src', $(this).attr('src'));
    })
});

var span = document.getElementsByClassName("close")[0];

span.onclick = function () {
    modal.style.display = "none";
}
/*
 * Modal - END
 ********************************************/


/*
 * Adjust Section When Resizing - START
 ********************************************/
var rtime;
var timeout = false;
var delta = 200;
$(window).resize(function () {
    showLoading()
    rtime = new Date();
    if (timeout === false) {
        timeout = true;
        setTimeout(resizeend, delta);
    }
});

$(window).on('orientationchange', function () {
    // Generate a resize event if the device doesn't do it
    window.dispatchEvent(new Event("resize"));
});

function resizeend() {
    if (new Date() - rtime < delta) {
        setTimeout(resizeend, delta);
    } else {
        timeout = false;
        updateProfileSectionPosition($('#profileNav .selected'));
        hideLoading();
    }
}
/*
 * Adjust Section When Resizing - END
 ********************************************/

/**
 * add click event to book btn
 */
$('#bookBtn').click(function () {
    var target = $('[data-target-section="profileSchedule"]');

    if (target.length > 0) {
        updateProfileSectionPosition(target);
    }
})

/**
 * add click event to event type filters
 */
$('.filter-event-type .btn').click(function () {
    // if the button that was clicked was already selected
    if ($(this).hasClass('selected'))
        return;

    var selectedEventType = $(this).data('event-type');
    $('.filter-event-type .btn.selected').removeClass('selected');
    $(this).addClass('selected');

    if (selectedEventType == 'all') {
        $('.profile-gallery-image').show();
    } else {
        $('.profile-gallery-image').each(function () {
            if ($(this).data('event-type') != selectedEventType) {
                $(this).hide();
            } else {
                $(this).show();
            }
        })
    }

    // adjust the height of the container when increasing/decreasing images
    $('#profileSectionsCont').css({
        height: $('#profileGallery').height()
    });
});

// adjust section container section nav base on number of sections
$(document).ready(function () {
    var sectionCount = $('.profile-sections').length;

    // setting the width of the section container base on number of profile sections there are
    $('#profileSectionsCont').css({
        width: sectionCount * 100 + 'vw'
    });

    // generating the section nav based on number of sections
    var profileNav = $('#profileNav');
    $('.profile-sections').each(function () {
        var sectionName = $(this).data('section-name');
        var classList = $(this).hasClass('default') ? 'profile-nav-optiions selected' : 'profile-nav-optiions';

        profileNav.append(
            $('<div></div>')
            .addClass(classList)
            .text($(this).data('section-name'))
            .attr('data-target-section', $(this).attr('id'))
            .css({
                width: 100 / sectionCount + '%'
            })
            .click(function () {
                updateProfileSectionPosition($(this))
            })
        )
    });

    // updating nav underline width
    $('#profileNavUnerline').css({
        width: 100 / sectionCount + '%'
    })

    // update the section nav underline posiiton
    updateProfileSectionPosition($('#profileNav .selected'));
});

/**
 * set the position of the profile navbar underline
 * 
 * @param {selector} target the profilenav child element
 */
function updateProfileSectionPosition(target) {
    var navPosition = target.position();

    $('#profileNav .selected').removeClass('selected');
    target.addClass('selected');

    $('#profileNavUnerline').css({
        left: navPosition.left
    });

    var sectionPos = $('#' + target.data('target-section')).position();

    $('#profileSectionsCont').css({
        left: sectionPos.left * -1,
        height: $('#' + target.data('target-section')).height()
    });
}