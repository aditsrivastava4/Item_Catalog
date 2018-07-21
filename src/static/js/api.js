function resgisterAPI() {
	$.post('/API/register', function(data) {

		if($('#key').val() == '') {
			renderAPI_form();
		}
		$('#key').attr('value', data);
		$('#keyButton').attr({
			'name': 'ReGenerate_Key',
			'value': 'Re-Generate Key'
		})
	});
}


function renderAPI_form() {
	$('#type_API').empty()
	type_API = '<label class="control-label col-sm-2">API:</label><div class="col-sm-10"><select id="API" class="form-control" name="api_type" onchange="renderCategory()" required>';
	type_API = type_API + '<option value="" selected disabled="">Select</option><option value="Catalog.json">Catalog.json</option>';
	type_API = type_API + '<option value="Category.json">Category.json</option><option value="Category_Items.json">Category Items.json</option>';
	type_API = type_API + '</select></div>';
	$('#type_API').removeAttr("style");
	$('#type_API').append(type_API);

	$('#requestButton').empty()
	button = '<div class="col-sm-offset-2 col-sm-10">'
	button = button + '<input class="btn btn-default" type="submit" name="Request" value="Request">'// onclick="request()"
	button = button + '<input class="btn btn-default" type="button" name="Cancel" value="Cancel" onclick = "cancel()"></div>'
	$('#requestButton').removeAttr("style");
	$('#requestButton').append(button);
}


function renderCategory() {
	//renderCategory
	var selected = $('#API').find(":selected").text();
	if(selected == 'Category Items.json') {
		$.post('/API/catalog/category.json', function(data) {
			var element = '<label class="control-label col-sm-2">Category:</label><div class="col-sm-10"><select id="selectCategory" class="form-control" name="category" required>';
			element = element + '<option value="" selected disabled="">Select</option>';

			for (var x = 0; x < data.length; x++) {
				element = element + '<option value="'+ data[x].category +'">'+ data[x].category +'</option>'
			}

			element = element + '</select></div>';
			$('#categories').removeAttr("style");//attr('style',"display: none;")
			$('#categories').append(element)
		});
	}
	else {
		$('#categories').empty()
		$('#categories').attr("style","display: none;")
	}
}

