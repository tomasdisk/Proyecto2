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
    if (data.now == "true") {
      //mostrar alerta
      $('#refreshAlert').html("");
    }
  });
}
