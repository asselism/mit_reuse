let map;
const DOME = {
    lat: 42.3598,
    lng: -71.0921
};
const CENTER = {
    lat: 42.359,
    lng: -71.095
}


function initMap() {
    let map = new google.maps.Map(document.getElementById('map'), {
        center: CENTER,
        zoom: 15,
        disableDefaultUI: true,
        styles: [
            {
                featureType: 'poi',
                stylers: [{visibility: 'off'}]
            }
        ]
    });
    let marker = new google.maps.Marker({ 
        map: map,
        position: DOME,
        title: 'Location',
        draggable: true
    });
    marker.addListener('drag', e => {
        pos = {lat: e.latLng.lat(), lng: e.latLng.lng()}
        console.log(pos);
    });
}
