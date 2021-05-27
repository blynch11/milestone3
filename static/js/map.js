function initMap() {
    let map = new google.maps.Map(document.getElementById("map"), {
        zoom: 7,
        center: {
            lat: 53.1424,
            lng: -7.6921
        }
    });

    let labels = "ABCDEFGHIJKLMONPQRSTUVWXYZ";

    let locations = [{
        lat: 53.3903,
        lng: -6.1548,
        location: "Hope",
    }, {
        lat: 52.2773,
        lng: -8.2696,
        location: "Eight Degrees",
    },  
    {
        lat: 54.9557,
        lng: -7.7061,
        location: "Kinnegar",
    }, 
    {
        lat: 53.3469,
        lng: -6.3751,
        location: "Whiplash",
    }, 
    {
        lat: 54.0893,
        lng: -8.5227,
        location: "White Hag",
    }, 
    {
        lat: 53.3394,
        lng: -6.3209,
        location: "Rascal",
    }, 
    {
        lat: 52.2773,
        lng: -8.2696,
        location: "Eight Degrees",
    }, 
    {
        lat: 52.2773,
        lng: -8.2696,
        location: "Eight Degrees",
    }, 
    ];

    let markers = locations.map(function(location, i) {
        let marker = new google.maps.Marker({
            position: location,
            label: labels[i % labels.length]
        });
        const infowindow = new google.maps.InfoWindow({
           content: location.location,
       });
       
       marker.addListener("click", () => {
           infowindow.open(map, marker);
       });
        return marker;
    });

    let markerCluster = new MarkerClusterer(map, markers, {
        imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'
    });
}