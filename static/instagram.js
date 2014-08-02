// Instantiate empty objects.
var Instagram = {};

var my_tags = [];

(function(){

  function filter_by_tag(photos){
    var dog_photos=[];
    $.each(photos.data, function(index, photo){
      try {
        for (i=0; i<photo.tags.length; i++) {
          console.log(photo.tags[i]);
          if (my_tags.indexOf(photo.tags[i]) >= 0 && dog_photos.indexOf(photo) === -1) {
            dog_photos.push(photo);
          }
        }
      } catch(err) {
        console.warn("photo won't load", photo.images.standard_resolution.url);
      }
    })
     
    toScreen(dog_photos);
  }


  function toScreen(photos){
    $.each(photos, function(index, photo){

      // Undefined function toTemplate, takes
      // the photo object and returns markup
      // ready for display.
      if (index === 0) {
      try{
        $('div.carousel-inner').append('<div class="item active"><img width=750 src='+ photo.images.standard_resolution.url + ' alt="Dog 1"></div>');
  
      }catch(err){
        console.warn("photo won't load", photo.images.standard_resolution.url);
      }
    }
      else {
    try{
        $('div.carousel-inner').append('<div class="item"><img width=800 class="full-screen-image" src='+ photo.images.standard_resolution.url + ' alt="Dog 1"></div>');
  
      }catch(err){
        console.warn("photo won't load", photo.images.standard_resolution.url);
      }

      }
    });
    $('.carousel').carousel();
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

