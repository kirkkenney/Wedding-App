function initMap() {
    var markerBaseURL = "http://maps.google.com/mapfiles/ms/icons/"
    var screenWidth = window.screen.width * window.devicePixelRatio;
    var zoomLevel;
    if (screenWidth <= 768) {
        zoomLevel = 10
    } else {
        zoomLevel = 10
    }
    var screenWidth = window.screen.width * window.devicePixelRatio;
    var zoomLevel;
    if (screenWidth <= 768) {
        zoomLevel = 10
    } else {
        zoomLevel = 10
    }
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: zoomLevel,
        center: new google.maps.LatLng(51.067389, 1.021885),
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControl: false,
        fullscreenControl: false
    });

    var marker, i

    // "locations" JSON is located in another Javascript file, and has been obfuscated
    // for privacy reasons

    for (i = 0; i < locations.length; i++) {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[i]["lat"], locations[i]["lon"]),
            icon: markerBaseURL + locations[i]["icon"],
            map: map
        });

        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                document.getElementById('mapText').innerHTML = locations[i]["name"] +
                '<br/>' + locations[i]["address"] + '<br/>' + locations[i]["postcode"] + '<br />' +
                locations[i]["url"]
            }
        })(marker, i));
    }
}


function loadScript() {
    var apiKey = 'AIzaSyAzZxxl7mFLRYjl2DkAeM_TCxFHP6Lnyvg'
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = 'https://maps.googleapis.com/maps/api/js?key='+apiKey+'&callback=initMap';
    document.getElementById('script').appendChild(script)
}

loadScript()
