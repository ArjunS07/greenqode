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
  
    function success(pos) {
      console.log("success");
      const crd = pos.coords;
  
      latitude = crd.latitude;
      longitude = crd.longitude;
      $("#map-picker").locationpicker("location", {latitude: latitude, longitude: longitude});
    }
    
    function error(err) {
      console.log("error");
      console.warn(`ERROR(${err.code}): ${err.message}`);
    }
  
    navigator.geolocation.getCurrentPosition(success, error);
    console.log(latitude);
    console.log(longitude);
    
  
    $("#map-picker").locationpicker("location", {latitude: latitude, longitude: longitude});
  
  
    });