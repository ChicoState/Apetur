showLoadingOnLoad();

/*
 * Adding second google map autocomplete - START
 ********************************************/
var input = document.getElementById('googleMapAutocompleteTextField');
var autocomplete = new google.maps.places.Autocomplete(input, options);

function redirect_to_profile(user_id) {
    location.replace(window.location.origin + "/profile?user_id=" + user_id);
}

google.maps.event.addListener(autocomplete, 'place_changed', function () {
    var data = {
        'lat': autocomplete.getPlace().geometry.location.lat(),
        'lng': autocomplete.getPlace().geometry.location.lng(),
        'r': document.getElementById("radius").value
    };
    location.replace(window.location.origin + "/browse?lat=" + data["lat"] + "&lng=" + data["lng"] +
        "&r=" +
        data["r"]);
})
/*
 * Adding second google map autocomplete - END
 ********************************************/

/**
 * toggle between profile list or map view on mobile at 768px
 */

// display both the profile list and map
function resetProfileMapCont() {
    if ($(window).innerWidth() <= 768) {
        $('#mapCont').hide();
        $('#browsePhotographers').show();
        $('#contentTypeToggle .fa-map-marked-alt').show();
        $('#contentTypeToggle .fa-user').hide();
    } else {
        $('#mapCont').show();
        $('#browsePhotographers').show();
    }
}

$('#contentTypeToggle').click(function () {
    $('#mapCont').toggle();
    $('#browsePhotographers').toggle();
    $('#contentTypeToggle .fa-map-marked-alt').toggle();
    $('#contentTypeToggle .fa-user').toggle();
});

var rtime;
var timeout = false;
var delta = 200;
var windowWidth = $(window).width();
$(window).resize(function () {
    rtime = new Date();
    if (timeout === false && $(window).width() != windowWidth) {
        showLoading()

        // Update the window width for next time
        windowWidth = $(window).width();
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
        resetProfileMapCont();
        hideLoading();
    }
}

/**
 * toggle for profile detail section
 */
$('.profile-breif-detail-toggle').click(function () {
    $(this).closest('.profile-brief-detail-cont')
        .siblings('.profile-brief-more-detail-cont')
        .slideToggle(250);

    $(this).find('.fas')
        .toggleClass('fa-angle-down fa-angle-up');
});