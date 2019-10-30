var options = {
    types: ['(cities)'],
    componentRestrictions: {
        country: "us"
    }
};
var input = document.getElementById('searchTextField');
var autocomplete = new google.maps.places.Autocomplete(input, options);


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