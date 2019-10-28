//  data_from_django = "{{photographers}}";
//   console.log(data_from_django);
function initMap() {
    var default_latitude = 39.728494;
    var default_longitude = -121.837478;
    if (!city_lat || !city_lng) {
        city_lat = default_latitude;
        city_lng = default_longitude;
    };
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: city_lat,
            lng: city_lng
        },
        zoom: 14
    });
    for (var i = 0; i < json_data.length; i++) {
        var marker = new google.maps.Marker({
            position: {
                lat: json_data[i]["lat"],
                lng: json_data[i]["lng"]
            },
            map: map,
            title: json_data[i]["name"]
        });
    }
}