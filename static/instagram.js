// Instantiate empty objects.
var Instagram = {};

(function(){

  function toScreen(photos){
    $.each(photos.data, function(index, photo){

      // Undefined function toTemplate, takes
      // the photo object and returns markup
      // ready for display.
      try{ 
        photo = "<img src='"+ photo.images.low_resolution.url + "' />";
        $('div#photos-wrap').append(photo);
      }catch(err){
        console.warn("photo won't load", photo.images.low_resolution.url);
      }


    });
  }

  function filter_by_tag(tag, data) {
    var filtered_data;
    // do filtering here
    debugger


    toScreen(filtered_data)
  }

  function search(tag){
    var url = "https://api.instagram.com/v1/users/180860648/media/recent?callback=?&client_id=aaf7cad994bd4ef293ed4ab24f2f6627" + tag + "/media/recent?callback=?&client_id=aaf7cad994bd4ef293ed4ab24f2f6627";
    // $.ajax({
    //   type: 'GET',
    //   url: url,
    //   dataType: 'jsonp',
    //   async: false,
    //   contentType: "application/json",
    //   success: function(data) {
    //     alert("hi");
    //   }
    // });
    $.getJSON(url, function (response) { 
      filter_by_tag(tag, response.data)
    });
  }


  Instagram.search = search;
})();

Instagram.search('barkcam');
