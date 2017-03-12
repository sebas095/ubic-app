/**
 * Created by sebastian on 10/03/17.
 */
let realTimeMarker, map;

function initMap() {
  const mapOptions = {
    zoom: 15,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  const googleCanvas = document.getElementById('google-canvas');
  map = new google.maps.Map(googleCanvas, mapOptions);

  navigator.geolocation.getCurrentPosition((position) => {
    const {latitude, longitude} = position.coords;
    const geolocation = new google.maps.LatLng(latitude, longitude);

    const marker = new google.maps.Marker({
      map: map,
      position: geolocation,
      visible: true
    });

    realTimeMarker = new google.maps.Marker({
      map: map,
      position: geolocation,
      visible: true
    });

    map.setCenter(geolocation);
    navigator.geolocation.watchPosition(updatePosition, console.log, {maximumAge: 0});
  }, console.log);
}

function updatePosition(position) {
  const {latitude, longitude} = position.coords;
  const geolocation = new google.maps.LatLng(latitude, longitude);
  realTimeMarker.setPosition(geolocation);
  map.setCenter(geolocation);
}