// focus on the textbox when clicked on the search button
$('.nav-search-cont').click(function () {
    $(this).closest('.form-control').focus();
})

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
            if ($('#settingDropdownCont .dropdown-toggle').attr("aria-expanded") == 'false') {
                $navbar_selector.addClass('show-color');
                $nav_show = true;
            }
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


/*
 * Settings dropdown behavior - START
 ********************************************/
$('#settingDropdownCont .dropdown-toggle').click(function () {
    if (!$nav_show) {
        if ($(this).attr("aria-expanded") == 'false') {
            $('.navstyle-semi-transparent').addClass('show-color');
        } else {
            $('.navstyle-semi-transparent').removeClass('show-color');
        }
    }
});

$('#settingDropdownCont .dropdown-menu').click(function (e) {
    e.stopPropagation();
});

$('#settingDropdownCont .user-profile-dropdown').click(function () {
    if ($(this).siblings('.dropdown-menu').is(':visible')) {
        $(this).siblings('.dropdown-menu')
            .slideUp(250);
    } else {
        $(this).closest('.dropdown')
            .trigger('show.bs.dropdown');
    }
    $(this).find('.fas').toggleClass('fa-angle-down fa-angle-up');
});
/*
 * Settings dropdown behavior - END
 ********************************************/


/*
 * Adding second google map autocomplete - START
 ********************************************/
var input2 = document.getElementById('googleMapAutocompleteTextField2');
var autocomplete2 = new google.maps.places.Autocomplete(input2, options);

google.maps.event.addListener(autocomplete2, 'place_changed', function () {
    var data = {
        'lat': autocomplete2.getPlace().geometry.location.lat(),
        'lng': autocomplete2.getPlace().geometry.location.lng(),
        'r': document.getElementById("radius2").value
    };
    location.replace(window.location.origin + "/browse?lat=" + data["lat"] + "&lng=" + data["lng"] +
        "&r=" +
        data["r"]);
})

$(window).on('load', function () {
    $('#googleMapAutocompletePacContainer').append($('.pac-container:eq(1)'));
})
/*
 * Adding second google map autocomplete - END
 ********************************************/