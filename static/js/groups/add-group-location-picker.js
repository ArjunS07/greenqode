$(function () {
  var latitude = 0;
  var longitude = 0;

  $("#map-picker").locationpicker({
    radius: 0,
    inputBinding: {
      latitudeInput: $("#lat"),
      longitudeInput: $("#lng"),
      locationNameInput: $("#location"),
    },
    enableAutocomplete: true,
    onchanged: function (currentLocation, radius, isMarkerDropped) {},
  });

  function success(pos) {
    const crd = pos.coords;

    latitude = crd.latitude;
    longitude = crd.longitude;
    $("#map-picker").locationpicker("location", {
      latitude: latitude,
      longitude: longitude,
    });
  }

  function error(err) {
  }

  navigator.geolocation.getCurrentPosition(success, error);

  $("#map-picker").locationpicker("location", {
    latitude: latitude,
    longitude: longitude,
  });
});
