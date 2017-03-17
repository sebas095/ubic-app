/**
 * Created by sebastian on 10/03/17.
 */
let map, ROUTE;
const COLORS_ARRAY = [
    "#0000FF", "#8A2BE2", "#A52A2A", "#000000", "#DEB887",
    "#5F9EA0", "#7FFF00", "#D2691E", "#FF7F50", "#6495ED",
    "#DC143C", "#00FFFF", "#00008B", "#008B8B", "#B8860B",
    "#A9A9A9", "#006400", "#8FBC8F", "#483D8B", "#9400D3",
    "#FFD700", "#008000", "#ADFF2F", "#87CEFA", "#00FF00"
];
let WAYPOINTS = [];
let DIRECTIONS_SERVICE = null;
let DIRECTIONS_DISPLAY = null;
let GEOCODER = null;

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
        console.log(position.coords);
        const {latitude, longitude} = position.coords;
        map = new google.maps.Map(document.getElementById('map'), {
            center: {
                lat: latitude,
                lng: longitude
            },
            zoom: 19
        });

        google.maps.event.addListener(map, 'click', (ev) => {
            console.log(ev.latLng);
            placeMarker(ev.latLng);
            WAYPOINTS.push([
                ev.latLng.lat(),
                ev.latLng.lng()
            ]);
        });
    });
}


function placeMarker(location) {
    const marker = new google.maps.Marker({
        position: location,
        map: map
    });
    //addNewPointToList(location);
}

function addNewPointToList(location) {
    const latlng = {
        lat: parseFloat(location.lat()),
        lng: parseFloat(location.lng())
    };

    GEOCODER.geocode({location: latlng}, (results, status) => {
        if (status === google.maps.GeocoderStatus.OK) {
            if (results[1]) {
                console.log(results);
                $("#content_routes").html($("#content_routes").html() +
                    `<li style="margin-bottom: 0px;min-height: 0px;height: 50px;border-bottom:1px solid #aaa;" class="mdl-grid mdl-grid--no-spacing mdl-shadow--2dp mdl-card mdl-cell mdl-cell--12-col">
                        <header style="width:50px;min-height:50px;" class="section__play-btn mdl-cell mdl-cell--3-col-desktop mdl-cell--2-col-tablet mdl-cell--4-col-phone mdl-color--teal-100 mdl-color-text--white">
                            <span style="font-size: 20pt;">3</span>
                        </header>
                        <div style="left: -80px;height: 50px;min-height: 50px;" class="mdl-card mdl-cell mdl-cell--5-col-desktop mdl-cell--6-col-tablet mdl-cell--4-col-phone">
                            <div style="margin-left: 10px;margin-top:0px;">
                                <span style="font-weight: bold;">Roberto Gomez</span><br>
                                <span style="font-size: 7pt">Dirección: ${results[0].formatted_address} </span>
                            </div>
                        </div>
                        <button class="mdl-button mdl-js-button mdl-js-ripple-effect mdl-button--icon" id="btn1" data-upgraded=",MaterialButton,MaterialRipple">
                            <i class="material-icons">more_vert</i>
                            <span class="mdl-button__ripple-container">
                                <span class="mdl-ripple is-animating" style="width: 92.5097px; height: 92.5097px; transform: translate(-50%, -50%) translate(24px, 19px);"></span>
                            </span>
                        </button>
                    </li>`
                );
            } else {
                alert('No results found');
            }
        } else {
            alert('Geocoder failed due to: ' + status);
        }
    });
}

function coordToText(coord) {
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

function displayRoute(response) {
    const routes = getLegsColors(response);
    routes.forEach(route => {
        new google.maps.DirectionsRenderer({
            suppressMarkers: true,
            map: map,
            directions: route.route,
            draggable: false,
            polylineOptions: {
                strokeColor: route.color
            }
        });
    });
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

function calcAndDisplayRoute(display) {
    DIRECTIONS_SERVICE.route({
        origin: coordToText((WAYPOINTS[0])),
        destination: coordToText(WAYPOINTS[WAYPOINTS.length - 1]),
        waypoints: createWayPoints(WAYPOINTS),
        travelMode: 'DRIVING',
        provideRouteAlternatives: false
    }, (response, status) => {
        if (status === 'OK') {
            if (display) displayRoute(response);
            ROUTE = response;
        } else {
            alert('Directions request failed due to ' + status);
        }
    });
}

$(function() {
    $("#content_routes").sortable();
    $('.client_route').click(function () {
        const $id = '#' + $(this).attr('id');
        const lat = $($id).children('input')[0].value.replace(',', '.');
        const lng = $($id).children('input')[1].value.replace(',', '.');
        const location = new google.maps.LatLng(lat, lng);
        placeMarker(location);
        console.log(location);
    })
});