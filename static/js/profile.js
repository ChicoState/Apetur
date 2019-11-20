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


var rtime;
var timeout = false;
var delta = 200;
$(window).resize(function () {
    rtime = new Date();
    if (timeout === false) {
        timeout = true;
        setTimeout(resizeend, delta);
    }
});

function resizeend() {
    if (new Date() - rtime < delta) {
        setTimeout(resizeend, delta);
    } else {
        timeout = false;
        updateProfileSectionPosition($('#profileNav .selected'));
    }
}

$('#profileNav').ready(function () {
    updateProfileSectionPosition($('#profileNav .selected'));
});


$('#profileNav > div').click(function () {
    updateProfileSectionPosition($(this));
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

    var sectionPos = $(target.data('target-section')).position();

    $('#profileSectionsCont').css({
        left: sectionPos.left * -1,
        height: $(target.data('target-section')).height()
    });
}

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
})