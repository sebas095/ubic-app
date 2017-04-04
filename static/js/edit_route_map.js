/**
 * Created by sebastian on 10/03/17.
 */
let map;
const COLORS_ARRAY = [
    "#0000FF", "#8A2BE2", "#A52A2A", "#000000", "#DEB887",
    "#5F9EA0", "#7FFF00", "#D2691E", "#FF7F50", "#6495ED",
    "#DC143C", "#00FFFF", "#00008B", "#008B8B", "#B8860B",
    "#A9A9A9", "#006400", "#8FBC8F", "#483D8B", "#9400D3",
    "#FFD700", "#008000", "#ADFF2F", "#87CEFA", "#00FF00"
];
const ROUTE = JSON.parse($('#id_directions').val());
let WAYPOINTS = [];
let DIRECTIONS_SERVICE = null;
let DIRECTIONS_DISPLAY = null;
let DISPLAY_ROUTES = [];
let GEOCODER = null;
let markers= [];
let count = 1;

window.addEventListener('load', initMap, false);

function initMap() {
    GEOCODER = new google.maps.Geocoder;
    DIRECTIONS_SERVICE = new google.maps.DirectionsService;
    DIRECTIONS_DISPLAY = new google.maps.DirectionsRenderer({
        draggable: false,
        polylineOptions: {
            strokeColor: "red"
        }
    });

    navigator.geolocation.getCurrentPosition(position => {
        const {latitude, longitude} = position.coords;
        map = new google.maps.Map(document.getElementById('map'), {
            center: {
                lat: latitude,
                lng: longitude
            },
            zoom: 19
        });

        const locations = getLocations(ROUTE);
        for (let i = 0; i < locations.length; i++) {
            const {lat, lng} = locations[i];
            const location = new google.maps.LatLng(lat, lng);
            markers.push(placeMarker(location, (i + 1).toString()));
        }

        DISPLAY_ROUTES = displayRoute(ROUTE);
    });
}


function placeMarker(location, label = '') {
    return new google.maps.Marker({
        position: location,
        label: label,
        map: map
    });
}


function coordToText(coord) {
    //console.log(coord);
    return coord[0] + ", " + coord[1];
}

function createWayPoints(array) {
    let wp = [];
    for (let i = 1; i < array.length - 1; i++) {
        wp.push({
            location: coordToText(array[i]),
            stopover: true
        });
    }
    return wp;
}

function displayRoute(response, flag = false) {
    const routes = getLegsColors(response);
    let displays = [];

    routes.forEach(route => {
        const display = new google.maps.DirectionsRenderer({
            suppressMarkers: true,
            map: map,
            directions: route.route,
            draggable: flag,
            polylineOptions: {
                strokeColor: route.color
            }
        });
        displays.push(display);
    });

    return displays;
}

function cloneObj(obj) {
    return JSON.parse(JSON.stringify(obj));
}

function getLegsColors(route) {
    let routes = [];
    if (route) {
        const {legs} = route.routes[0];
        for (let i = 0; i < legs.length; i++) {
            const newRoute = cloneObj(route);
            newRoute.routes[0].legs = [];
            newRoute.routes[0].legs.push(cloneObj(legs[i]));
            routes.push({
                color: COLORS_ARRAY[i],
                route: newRoute
            });
        }
    }
    return routes;
}

function getUniqueLocations(locations) {
    let results = {};
    let uniqueLocations = [];
    let index = 0;

    for (let i = 0; i < locations.length; i++) {
        const location = locations[i];
        results[location.lat + ' - ' + location.lng] = location;
    }

    for(let location in results) {
        uniqueLocations[index++] = results[location];
    }

    return uniqueLocations;
}

function getLocations(route) {
    let locations = [];
    if (route) {
        const {legs} = route.routes[0];
        for (let i = 0; i < legs.length; i++) {
            locations.push(legs[i].start_location);
            locations.push(legs[i].end_location);
       }
   }
   return getUniqueLocations(locations);
}

function calcAndDisplayRoute(display) {
    DIRECTIONS_SERVICE.route({
        origin: coordToText((WAYPOINTS[0])),
        destination: coordToText(WAYPOINTS[WAYPOINTS.length - 1]),
        waypoints: createWayPoints(WAYPOINTS),
        travelMode: 'DRIVING',
        provideRouteAlternatives: false
    }, (response, status) => {
        if (status === 'OK') {
            response = ROUTE;
            if (display) DISPLAY_ROUTES = displayRoute(response);
            id_clients = [];

            const clients = document.querySelectorAll('.client_route');
            for (let cl = 0; cl < clients.length; cl++) {
                const client = clients[cl];
                if (client.getAttribute('data-client')) {
                    const index = Number(client.getAttribute('data-client')) - 1;
                    id_clients[index] = Number(client.id);
                }
            }

            document.getElementById('id_meta_clients').value = JSON.stringify(id_clients);
            document.getElementById('id_directions').value = JSON.stringify(ROUTE);
            document.getElementById('route_form').submit();
        } else {
            alert('Directions request failed due to ' + status);
        }
    });
}

function displayClientRoute(ev) {
    const $id = '#' + $(this).attr('id');
    const lat = parseFloat($($id).children('input')[0].value.replace(',', '.'));
    const lng = parseFloat($($id).children('input')[1].value.replace(',', '.'));
    const location = new google.maps.LatLng(lat, lng);
    const div = $($id).children('div')[1];

    if (!$(div).children().text()) {
        WAYPOINTS.push([
            lat,
            lng
        ]);

        $(div).addClass('selected');
        $(div).children().text(`${count++}`);
        $($id).attr('data-client', count - 1);
        $(div).css('background-color', '#66BAB8');
        markers.push(placeMarker(location, (count - 1).toString()))
    }
}

function clearRoute() {
    for (let i = 0; i < markers.length; i++) {
        if (markers[i]) markers[i].setMap(null);
        if (DISPLAY_ROUTES[i]) DISPLAY_ROUTES[i].setMap(null);
    }

    markers = [];
    DISPLAY_ROUTES = [];
    WAYPOINTS = [];
    count = 1;

    $('.selected')
        .css('background-color', '#fff')
        .children('div')
        .text('')
        .removeClass('selected');
}

$(function() {
    $('#content_routes').sortable();
    $('.client_route').click(displayClientRoute);
    $('#clear_route').click(clearRoute);
});