function send_ItemAPI() {
	var data = $('#set').find(":selected").text();
	if(data!='Select') {
		window.location.href = 'API/' + data +'/items.json';
	}
}
function resgisterAPI() {
	$.post('/API/register', function(data) {
		$('#key').attr('value', data);
	});
}

function renderCategory() {
	//renderCategory
}