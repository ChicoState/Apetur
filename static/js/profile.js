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