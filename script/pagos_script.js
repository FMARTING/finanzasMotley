var main = function() {
    $('.jugador').prop('disabled', true);
	$('.propio').prop('checked', true);
	$('form').submit(function(event){
		if (confirm("Estas seguro que queres ingresar este pago?")){
			return;
		}
		event.preventDefault();
	});
};
var text_analyzer = function() {
	if ($('.otro').is(':checked')){
		$('.jugador').prop('disabled', false);}
	else{
		$('.jugador').prop('disabled', true);}
};

$(document).ready(main);
$(":radio").on("change", text_analyzer);
/*
<script>
$( "form" ).submit(function( event ) {
  if ( $( "input:first" ).val() === "correct" ) {
    $( "span" ).text( "Validated..." ).show();
    return;
  }
 
  $( "span" ).text( "Not valid!" ).show().fadeOut( 1000 );
  event.preventDefault();
});
</script>
*/