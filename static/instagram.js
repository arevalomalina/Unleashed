alert ("TOP");// Instantiate empty objects.
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

  function search(tag){
    var url = "https://api.instagram.com/v1/tags/" + tag + "/media/recent?callback=?&client_id=aaf7cad994bd4ef293ed4ab24f2f6627";
    $.getJSON(url, toScreen);
  }


  Instagram.search = search;
})();

Instagram.search('barkcam');
alert ("botton");