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
    })
});

$('.carousel').carousel({
  interval: false
})
