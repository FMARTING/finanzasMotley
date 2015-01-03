var main = function() {
	$('form').submit(function(event){
		if (confirm("Estas seguro que queres ingresar esta informacion?")){
			return;
		}
		event.preventDefault();
	});
};

$(document).ready(main);