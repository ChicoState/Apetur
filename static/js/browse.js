/*
 * Adding second google map autocomplete - START
 ********************************************/
var input = document.getElementById('googleMapAutocompleteTextField');
var autocomplete = new google.maps.places.Autocomplete(input, options);

function redirect_to_profile(user_id){
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