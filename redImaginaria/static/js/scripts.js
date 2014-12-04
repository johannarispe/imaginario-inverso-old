$(function() {
var submit_form = function(e) {
	//$.getJSON($SCRIPT_ROOT + '/_conversar', {
	$.getJSON('http://inverso.local:5000/_conversar', {
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

	$.updater({
		//url: $SCRIPT_ROOT + '/_mensajes',
		url: 'http://inverso.local:5000/_mensajes',
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
