$(document).ready(function () {
	$('#drinkingCircliful').circliful({
		getText: function () {
			if (this.usesTotal())
				return Math.round(this.getCurrentValue());
			else
				return this.getCurrentValue();
		},
		getInfoText: function () {
			return "Drinking Water";
		},
		'dimension': 200,
		'background-fill-color': '#fff',
		'background-radius': 85,
		'foreground-radius': 95,
		'background-width': 15,
		'background-stroke-color': '#808080',
	});
	$('#drinkingCircliful').circliful('animateToValue', 0);
});
$(document).ready(function () {
	$('#plantCircliful').circliful({
		getText: function () {
			if (this.usesTotal())
				return Math.round(this.getCurrentValue());
			else
				return this.getCurrentValue();
		},
		getInfoText: function () {
			return "Plant Water";
		},
		'dimension': 200,
		'background-fill-color': '#fff',
		'background-radius': 85,
		'foreground-radius': 95,
		'background-width': 15,
		'background-stroke-color': '#808080',
	});
	$('#plantCircliful').circliful('animateToValue', 0);
});
$(document).ready(function () {
	$('#bathingCircliful').circliful({
		getText: function () {
			if (this.usesTotal())
				return Math.round(this.getCurrentValue());
			else
				return this.getCurrentValue();
		},
		getInfoText: function () {
			return "Bathing Water";
		},
		'dimension': 200,
		'background-fill-color': '#fff',
		'background-radius': 85,
		'foreground-radius': 95,
		'background-width': 15,
		'background-stroke-color': '#808080',
	});
	$('#bathingCircliful').circliful('animateToValue', 0);
});

$(document).ready(function () {
	$('#carCircliful').circliful({
		getText: function () {
			if (this.usesTotal())
				return Math.round(this.getCurrentValue());
			else
				return this.getCurrentValue();
		},
		getInfoText: function () {
			return "Car Wash";
		},
		'dimension': 200,
		'background-fill-color': '#fff',
		'background-radius': 85,
		'foreground-radius': 95,
		'background-width': 15,
		'background-stroke-color': '#808080',
	});
	$('#carCircliful').circliful('animateToValue', 0);
});

let myObser = Rx.Observable.timer(0, 10000).map(() => fetch(`/users/dataUpdate/`).then(res => res.json()))
myObser.subscribe(x => x.then(data => {

	document.getElementById("time").innerHTML = data.time;
	document.getElementById("date").innerHTML = data.date;

	var drinking_lcolor, drinking_level = data.drinking_distance;
	if (drinking_level <= 35) drinking_lcolor = '#f00';
	else drinking_lcolor = '#0f0';

	var plant_lcolor, plant_level = data.plant_distance;
	if (plant_level <= 35) plant_lcolor = '#f00';
	else plant_lcolor = '#0f0';

	var bathing_lcolor, bathing_level = data.bathing_distance;
	if (bathing_level <= 35) bathing_lcolor = '#f00';
	else bathing_lcolor = '#0f0';

	var car_lcolor, car_level = data.car_distance;
	if (car_level <= 35) car_lcolor = '#f00';
	else car_lcolor = '#0f0';


	$('#drinkingCircliful').circliful('animateToValue', drinking_level);
	$('#drinkingCircliful').circliful('setSetting', 'foreground-color', drinking_lcolor);
	$('#plantCircliful').circliful('animateToValue', plant_level);
	$('#plantCircliful').circliful('setSetting', 'foreground-color', plant_lcolor);
	$('#bathingCircliful').circliful('animateToValue', bathing_level);
	$('#bathingCircliful').circliful('setSetting', 'foreground-color', bathing_lcolor);
	$('#carCircliful').circliful('animateToValue', car_level);
	$('#carCircliful').circliful('setSetting', 'foreground-color', car_lcolor);

	var temperature_data = String(data.temperature);
	var humidity_data = String(data.humidity);
	var pH_data = String(data.pH);
	var turbidity_data = String(data.turbidity);
	var type_of_water_data = "Type of Water : " + String(data.type_of_water);

	document.getElementById('current_temperature').innerHTML = temperature_data;
	document.getElementById('current_humidity').innerHTML = humidity_data;
	document.getElementById('current_pH').innerHTML = pH_data;
	document.getElementById('current_turbidity').innerHTML = turbidity_data;
	document.getElementById('current_type_of_water').innerHTML = type_of_water_data;

	if(data.drinkingWaterActuatorStatus == true)
		document.getElementById(12).checked = true;
	else
		document.getElementById(12).checked = false;

	if(data.carWaterActuatorStatus == true)
		document.getElementById(16).checked = true;
	else
		document.getElementById(16).checked = false;

	if(data.bathingWaterActuatorStatus == true)
		document.getElementById(20).checked = true;
	else
		document.getElementById(20).checked = false;

	if(data.plantWaterActuatorStatus == true)
		document.getElementById(21).checked = true;
	else
		document.getElementById(21).checked = false;

	actuator_tab(data.actuator_control, data.actuator_link);
}
))

function actuator_control(value, checked)
{
	console.log(value, checked);
	$.ajax({
		url: "http://192.168.43.97:8000/users/controlActuator/",
		type: "POST",
		dataType: 'json',
		data: { 'value': value, 'action': checked, "csrfmiddlewaretoken": '{{ csrf_token }}' },
		success: data => {
			console.log(data);
			if(data.success)
				console.log('yes');
			else if(data.success == 0){
				alert('Cannot connect too Actuators. Kindly check your Internt Connections');
				document.getElementById(value).checked = !checked;
			}
		},
		error: data => {
		}
	});
}

function actuator_tab(actuatorcontrol, actuatorlink) {
	if (actuatorlink == -1) {
		document.getElementById("block1").style.opacity = 0.3;
		document.getElementById("err1").style.display = "block";
	}
	else {
		document.getElementById("block1").style.opacity = 1;
		document.getElementById("err1").style.display = "none";
		if (actuatorcontrol == 0) {
			document.getElementById("block2").style.opacity = 0.2;
			document.getElementById("err2").style.display = "block";
		}
		else {
			document.getElementById("block2").style.opacity = 1;
			document.getElementById("err2").style.display = "none";
		}
	}
}