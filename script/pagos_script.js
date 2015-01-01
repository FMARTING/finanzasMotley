var main = function() {
    $('.jugador').prop('disabled', true);
	$('.propio').prop('checked', true);
	$('#ingresar_pago').click(function(){
		if(confirm('Estas seguro de querer ingresar este pago?')){
			$('form#pago').submit();
		}
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