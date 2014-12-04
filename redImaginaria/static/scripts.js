$(function() {
var submit_form = function(e) {
	$.getJSON($SCRIPT_ROOT + '/_conversar', {
		mensaje: $('#mensaje').val()
	}, function(data) {
		$('input[name=mensaje]').focus().select();
		$('#mensajes ul').append(
			$('<li>').append(		
			$('<p>').append(
			$('<span>').attr('class', 'mensajeTX').append(data.time+" : "+data.mensaje)
		)));
		
		$('#mensaje').val('');
	 });
	 return false;
};
	$('#enviar').bind('click', submit_form);
	$('input[type=text]').bind('keydown', function(e) {
		if (e.keyCode == 13) {
			submit_form(e);
		}
		});
	$('input[name=mensaje]').focus();
});

//$(document).ready(function(){
//	    setInterval(refreshMensajes, 5000);
//$(fucntion(){
	$.updater({
		//url: $SCRIPT_ROOT + '/_recibir',
		url: '/static/test.json',
		method: 'get',
		interval: 1500
	},
	function(data, response){
		console.log(response);
		$('#mensajes ul').append(
			$('<li>').append(
			$('<p>').append(
			$('<span>').attr('class', 'mensajeRX').append(data.name)
		)));
	});
//});
//});

function refreshMensajes(){
	$.getJSON($SCRIPT_ROOT + '/_recibir',function(data) {
	$('#mensajes ul').append(
        	$('<li>').append(
	        $('<p>').append(
	        $('<span>').attr('class', 'mensajeRX').append(data.mensaje)
	)));
	});
}
