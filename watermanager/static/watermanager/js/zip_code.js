$( document ).ready(function() {
	var zipCode = "";
	var length = $('#weather-list li').length;
	console.log("There are " + length + " in the list.");
	$('#weather-list li').each(function(){
   		var plantID = $(this).attr("id");
		console.log(plantID);
		if (plantID != undefined) {
			zipCode = document.getElementById("plant-"+plantID).value;
			$.ajax({
				url: "http://api.zippopotam.us/us/" + zipCode,
				cache: false,
				dataType: "json",
				type: "GET",
			    success: function(result, success) {
					// US Zip Code Records Officially Map to only 1 Primary Location
					places = result['places'][0];
					$("#city-"+plantID).val(places['place name']);
					$("#state-"+plantID).val(places['state']);
					var city = places['place name'];	
					var state = places['state'];	
					var place = city + ", " + state; 
					$.simpleWeather({
						location: place,
						woeid: '',
						unit: 'f',
						success: function(weather) {
						  html = '<h2><i class="icon-'+weather.code+'"></i> '+weather.temp+'&deg;'+weather.units.temp+'</h2>';
						  html += '<ul><li>'+weather.city+', '+weather.region+'</li>';
						  html += '<li class="currently">'+weather.currently+'</li>';
						  html += '<li>'+weather.wind.direction+' '+weather.wind.speed+' '+weather.units.speed+'</li></ul>';
						  $("#weather-"+plantID).html(html);
						},
						error: function(error) {
						  $("#weather-"+plantID).html('<p>'+error+'</p>');
						}
						});
				},
				error: function(result, success) {
					zip_box.removeClass('success').addClass('error');
				}
			});
		}
	});		
});	
