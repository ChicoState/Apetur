var options = {
    types: ['(cities)'],
    componentRestrictions: {
        country: "us"
    }
};
var navbarInput = document.getElementById('googleMapAutocompleteTextFieldNavbar');
var navbarAutocomplete = new google.maps.places.Autocomplete(navbarInput, options);

google.maps.event.addListener(navbarAutocomplete, 'place_changed', function () {
    var data = {
        'lat': navbarAutocomplete.getPlace().geometry.location.lat(),
        'lng': navbarAutocomplete.getPlace().geometry.location.lng(),
        'r': document.getElementById("navbarRadius").value
    };
    location.replace(window.location.origin + "/browse?lat=" + data["lat"] + "&lng=" + data["lng"] +
        "&r=" +
        data["r"]);
})

/*
 * Adding second google map autocomplete - START
 ********************************************/
var navbarInput2 = document.getElementById('googleMapAutocompleteTextFieldNavbar2');
var navbarAutocomplete2 = new google.maps.places.Autocomplete(navbarInput2, options);

google.maps.event.addListener(navbarAutocomplete2, 'place_changed', function () {
    var data = {
        'lat': navbarAutocomplete2.getPlace().geometry.location.lat(),
        'lng': navbarAutocomplete2.getPlace().geometry.location.lng(),
        'r': document.getElementById("navbarRadius2").value
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