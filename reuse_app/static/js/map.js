let map;
const CENTER = {
    lat: 42.359,
    lng: -71.095
}

function get_input_coordinates() {
    let ans = {
        'lat': parseFloat($('#id_loc_lat')[0].value),
        'lng': parseFloat($('#id_loc_lng')[0].value)
    };
    console.log(ans);
    return ans;
}

function set_input_coordinates(coord) {
    $('#id_loc_lat')[0].value = coord['lat'].toFixed(6);
    $('#id_loc_lng')[0].value = coord['lng'].toFixed(6);
}

function init_map() {
    map = new google.maps.Map(document.getElementById('map'), {
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
}

function init_update_view() {
    init_map();
        
    let marker = new google.maps.Marker({ 
        map: map,
        position: get_input_coordinates(),
        draggable: true
    });
    marker.addListener('drag', e => {
        pos = {lat: e.latLng.lat(), lng: e.latLng.lng()}
        set_input_coordinates(pos);
    });
}

function init_details_view() {
    init_map();

    let marker = new google.maps.Marker({ 
        map: map,
        position: listing_coordinates,
    });
}

function init_list_view() {
    init_map();
    let infoWindow = null;
    for (let listing of listings) {
        let marker = new google.maps.Marker({
            map: map,
            position: {
                'lat': listing['lat'],
                'lng': listing['lng']
            },
            title: listing['title']
        });
        marker.addListener('click', () => {
            if (infoWindow) {
                infoWindow.close();
            }
            infoWindow = new google.maps.InfoWindow({
                content: '<h2>' + listing['title'] + '</h2>'
            });
            infoWindow.open(map, marker);
        });
    }
}
