kr = {'last_places_api_response': new Date('01.01.1900')};

kr.buildMap = function(target_div, center, zoom, use_geolocate){
    var osm_layer = new OpenLayers.Layer.OSM("OSM Map Layer");
    kr.map = new OpenLayers.Map({
        div: target_div,
        layers: [osm_layer],
        center: center,
        zoom: zoom
    });

    // Base marker layer
    kr.markers = new OpenLayers.Layer.Markers( "Markers" );
    kr.map.addLayer(kr.markers);

    kr.marker_icons = {
        'default': [STATIC_URL + 'icons/pin.png', new OpenLayers.Size(15, 24)],
        'christian': [STATIC_URL + 'icons/christianity_church.png', new OpenLayers.Size(24, 25)],
        'islam': [STATIC_URL + 'icons/islam.png', new OpenLayers.Size(25, 24)],
        'muslim': [STATIC_URL + 'icons/islam.png', new OpenLayers.Size(25, 24)],
        'hindu': [STATIC_URL + 'icons/hindu.png', new OpenLayers.Size(24, 24)],
        'budddhist': [STATIC_URL + 'icons/buddhist.png', new OpenLayers.Size(28, 22)]
    };

    for (var name in kr.marker_icons) {
        var url = kr.marker_icons[name][0];
        var size = kr.marker_icons[name][1];
        kr.marker_icons[name] = new OpenLayers.Icon(
            url,
            size,
            new OpenLayers.Pixel(-(size.w/2), -size.h)
        );
    }

    // Geolocation
    if (use_geolocate) {
        var geolocate = new OpenLayers.Control.Geolocate({
            bind: true
        });
        geolocate.events.register("locationupdated", geolocate, function(e) {
            kr.map.zoomTo(13);
        });

        kr.map.addControl(geolocate);
        geolocate.activate();
    }

    kr.on_marker_click = function(e){
       window.location = "/" + e.object.place_id;
    };

    kr.refresh_markers = function(){
        $.getJSON("/api/v1/places/?epsg=900913&in_bbox=" + kr.map.getExtent().toBBOX(), function(response, status, xhr){
            response_date = new Date(xhr.getResponseHeader('Date'));
            if (response_date > kr.last_places_api_response) {
                kr.markers.clearMarkers();
                for (var i in response.places_of_worship) {
                    place = response.places_of_worship[i];

                    var icon;
                    if (place.religion in kr.marker_icons) {
                        icon = kr.marker_icons[place.religion].clone();
                    } else {
                        icon = kr.marker_icons['default'].clone();
                    }

                    var marker = new OpenLayers.Marker(new OpenLayers.LonLat(place.lon, place.lat), icon);
                    marker.place_id = place.id;

                    if (place.name === null) {
                        place.name = "unknow";
                    }
                    if (place.religion === null) {
                        place.religion = "unknow";
                    }
                    tooltip = OpenLayers.String.format("${name} (${religion})", place);

                    $(marker.events.element).tooltip({
                        'title': tooltip
                    });

                    marker.events.register("click", marker, kr.on_marker_click);

                    kr.markers.addMarker(marker);
                }
                kr.last_places_api_response = new Date(xhr.getResponseHeader('Date'));
            }
        });
    };

    kr.map.events.register("moveend", map, kr.refresh_markers);
};