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

var show = false;
var c = 1;

// ejecucion periodica de refreshData si hay un usuario logueado
jQuery(document).ready(function(){
  if($('#logged').data('logged')===true){
    setInterval(function(){
      refreshData();
    }, 4000);
  }
});
// obtener nuevos datos JSON con AJAX y actualizarlos en la pagina
function refreshData(){
  $.getJSON("/refreshData", function(data){
    // aplicar cambios
    if (data.new == "true") {
      if (($('#myModal').data('bs.modal') || {}).isShown) {
        show = true;
      }
      //ocultar alerta anterior
      $('#myModal').modal('toggle');
      //insertar info en el modal
      if (data.known == "true") {
        $('#modalBody').html('Se ha detectado un nuevo ingreso de la Vaca: ' + data.picc + '<br>¿Desea ver el detalle?');
        $('#modalButton').html('<a href="/cow/' + data.picc + '" class="btn btn-success" role="button">Ver Vaca</a>');
      }
      else {
        $('#modalBody').html('Se ha detectado una Vaca sin informacion en el sistema.<br>Código detectado: ' + data.picc + '<br>¿Desea ingresar los datos ahora?');
        $('#modalButton').html('<a href="/newCow?picc=' + data.picc + '" class="btn btn-warning" role="button">Añadir Vaca</a>');
      }
      c++;
    }
  });
}

// una vez que el modal se oculto
$('#myModal').on('hidden.bs.modal', function (e) {
  // si hay que mostrarlo devuelta lo vuelve a activar
  if (show === true){
    $('#myModal').modal('show');
    show = false;
  }
});
