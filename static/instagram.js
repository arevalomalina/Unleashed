// Instantiate empty objects.
var Instagram = {};

var my_tags = [];

(function(){

  function filter_by_tag(photos){
    var money_shots=[];
    $.each(photos.data, function(index, photo){
      try {
        for (i=0; i<photo.tags.length; i++) {
          console.log(photo.tags[i]);
          if (my_tags.indexOf(photo.tags[i]) >= 0 && money_shots.indexOf(photo) === -1) {
            money_shots.push(photo);
          }
        }
      } catch(err) {
        console.warn("photo won't load", photo.images.low_resolution.url);
      }
    })
    toScreen(money_shots);
  }


  function toScreen(photos){
    $.each(photos, function(index, photo){

      // Undefined function toTemplate, takes
      // the photo object and returns markup
      // ready for display.
      try{ 
        photo_html = "<img src='"+ photo.images.low_resolution.url + "' />";
        $('div#photos-wrap').append(photo_html);
      }catch(err){
        console.warn("photo won't load", photo.images.low_resolution.url);
      }


    });
  }

  function search(tags){

    my_tags = tags;

    var malina_id = '12764357';
    var ida_id = '180860648';
    var id_to_use = malina_id;

    var url = "https://api.instagram.com/v1/users/" + id_to_use + "/media/recent?callback=?&client_id=aaf7cad994bd4ef293ed4ab24f2f6627";
    //  + tag + "/media/recent?callback=?&client_id=aaf7cad994bd4ef293ed4ab24f2f6627";
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
    $.getJSON(url, filter_by_tag);
  }


  Instagram.search = search;
})();

