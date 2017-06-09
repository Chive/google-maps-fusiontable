function Map(element, urlConfig, csrfToken) {
    this.markers = {};

    this.urlConfig = urlConfig;
    this.map = new google.maps.Map(
        element, {
            zoom: 9,
             // Zurich
            center: {
                lat: 47.3773697,
                lng: 8.3966342
            }
        }
    );
    this.csrfToken = csrfToken;

    this.setupListeners();
    this.updateLocationList();
}

Map.prototype.setupListeners = function() {
    var that = this;

    // coordinates lookup
    this.map.addListener('click', function(event) {
        var latitude = event.latLng.lat();
        var longitude = event.latLng.lng();
        var marker = that.addMarker(latitude, longitude);

        // send coordinates lookup to backend
        jQuery.post({
            url: that.urlConfig.lookupCoordinates,
            data: {
                latitude: latitude,
                longitude: longitude,
                csrfmiddlewaretoken: that.csrfToken
            },
            success: function(data) {
                if (data.success) {
                    if (data.status === 'DUPLICATE_LOCATION') {
                        $.notify('Location already geocoded.', 'warning');
                    } else {
                        that.updateLocationList();
                    }
                } else {
                    if (data.status === 'UNABLE_TO_UPDATE_FUSIONTABLE') {
                        $.notify(
                            'There was an error while trying to update Fusion table. ' +
                            'Please try again later.',
                            'error'
                        );
                    } else {
                        $.notify('Unable to geocode, please try again.', 'warning');
                    }
                    if (marker) {
                        marker.setMap(null);
                    }
                }
            },
            error: function(data) {}

        })
    });
};

Map.prototype.updateLocationList = function() {
    var that = this;
    // get location list from backend and render as a table
    jQuery.ajax({
        url: that.urlConfig.getLocations,
        success: function(data) {
            var rawLocations = data.locations;

            var html = (
                '<tr>' +
                '<th>Address</th>' +
                '<th>Latitude</th>' +
                '<th>Longitude</th>' +
                '</tr>'
            );

            for (var i = 0; i < rawLocations.length; i++) {
                var location = new Location(rawLocations[i]);
                html += location.render();
                that.addMarker(location.latitude, location.longitude);
            }

            $('#locations-table').html(html);
        }
    })
};

Map.prototype.clearLocationList = function() {
    var that = this;

    // clear the saved locations
    jQuery.post({
        url: that.urlConfig.clearLocations,
        data: {
            csrfmiddlewaretoken: that.csrfToken
        },
        success: function(data) {
            $.notify('Locations have been cleared!', 'success');
            that.updateLocationList();
            that.clearMarkers();
        }
    })
};

Map.prototype.addMarker = function(latitude, longitude) {
    var markerKey = String(latitude) + ',' + String(longitude);
    if (!(markerKey in this.markers)) {
        var marker = new google.maps.Marker({
            position: {
                lat: latitude,
                lng: longitude
            },
            map: this.map
        });
        this.markers[markerKey] = marker;
        return marker;
    }
};


Map.prototype.clearMarkers = function() {
    for (var key in this.markers) {
        this.markers[key].setMap(null);
    }
};