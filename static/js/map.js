//  data_from_django = "{{photographers}}";
//   console.log(data_from_django);
function initMap() {
    default_latitude = 39.728494;
    default_longitude = -121.837478;
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: default_latitude,
            lng: default_longitude
        },
        zoom: 14
    });
}