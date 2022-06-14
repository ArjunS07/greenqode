$(function () {
  var latitude = $("#lat").val();
  var longitude = $("#lng").val();

  $("#map-picker").locationpicker({
    location: {latitude: latitude, longitude: longitude},
    radius: 0,
    inputBinding: {
      latitudeInput: $("#lat"),
      longitudeInput: $("#lng"),
      locationNameInput: $("#location"),
    },
    enableAutocomplete: true,
    onchanged: function (currentLocation, radius, isMarkerDropped) {
      alert(
        "Location changed. New location (" +
          currentLocation.latitude +
          ", " +
          currentLocation.longitude +
          ")"
      );
    },
  });
});
