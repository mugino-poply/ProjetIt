$('select').on('input', function(){
  $('img').attr('src', $('select').find(':selected').attr('image'));
});