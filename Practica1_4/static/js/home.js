// 'Back To Top' floating button
jQuery(document).ready(function() {
    // offsetTop hasta que aparesca
    var offset = 220;
    // duracion del scrollUp
    var duration = 500;
    // mostrar boton
    jQuery(window).scroll(function() {
        if (jQuery(this).scrollTop() > offset) {
            jQuery('.back-to-top').fadeIn(duration);
        } else {
            jQuery('.back-to-top').fadeOut(duration);
        }
    });
    // boton clickeable
    jQuery('.back-to-top').click(function(event) {
        event.preventDefault();
        jQuery('html, body').animate({scrollTop: 0}, duration);
        return false;
    });
});

// ejecucion periodica de refreshData si hay un usuario logueado
jQuery(document).ready(function(){
  if($('#logged').data('logged')===true){
    setInterval(function(){
      refreshData();
    }, $('#freq').data('freq')*1000);
  }
});

// obtener nuevos datos JSON con AJAX y actualizarlos en la pagina
function refreshData(){
  $.getJSON("/refreshData", function(data){
    // aplicar cambios
    $('#temp_sample').html(data.temp_sample);
    $('#temp_avg').html(data.temp_avg);
    $('#hum_sample').html(data.hum_sample);
    $('#hum_avg').html(data.hum_avg);
    $('#pres_sample').html(data.pres_sample);
    $('#pres_avg').html(data.pres_avg);
    $('#wind_sample').html(data.wind_sample);
    $('#wind_avg').html(data.wind_avg);
  });
}
