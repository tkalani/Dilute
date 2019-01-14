from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from users.models import *
import json
import requests
from django.db import connection


# Create your views here.

@csrf_exempt
def mobile_login(request):
	if request.method=='POST':
		print("post successfull")
		jsonResponse=json.loads(request.body.decode('utf-8'))
		mob_no=jsonResponse['json_data']['username']
		password=jsonResponse['json_data']['password']
		user_prof = get_object_or_404(UserProfile, mob_no=mob_no)
		user = authenticate(username=mob_no, password=password)
		print ("user is ", user)
		if user is not None:
			# login(request, user)
			print("App- True")
			print (user_prof)
			return JsonResponse({"pass":"true","name":user_prof.name,"email":user_prof.email,"address":user_prof.address,"vehicles":user_prof.vehicles, "members":user_prof.members, "plants":user_prof.plants,"mainTank_capacity":user_prof.mainTank_capacity, "quantumTank_capacity":user_prof.quantumTank_capacity, "carWater_capacity":user_prof.carWater_capacity, "bathingWater_capacity":user_prof.bathingWater_capacity, "plantWater_capacity":user_prof.plantWater_capacity, "drinkingWater_capacity":user_prof.drinkingWater_capacity})
			# return HttpResponseRedirect('../main')
		else:
			print("App- False")
			return JsonResponse({"pass":"false"})
			# return HttpResponse("Wrong Mobile Number Or Password")


	# 	print("Authentic")
	# 	print(password)
	# 	t = Users.objects.filter(password=password,phone=username)

	# 	if len(t):
	# 		print("Authentic")
	# 		#request.session['name'] = t[0].name
	# 		#request.session['id'] = t[0].id

	# 		global userid
	# 		userid = t[0].id
	# 		u={"pass":"true","id":t[0].id,"name":t[0].name,"phone":t[0].phone,"address":t[0].address,"currentplant":t[0].currentplant}
	# 		print(u)
	# 		return JsonResponse(u)
	# 	else:
	# 		u={"pass":"false"}
	# 		print(u)
	# 		return JsonResponse(u)
	if request.method=='GET':
		return HttpResponse("<h1>hi</h1>")

@csrf_exempt
def getQuantityDetailsurl(request):
	jsonResponse=json.loads(request.body.decode('utf-8'))
	email = jsonResponse['email']
	print "quantity = ", email
	user = User.objects.get(email = email)
	data = CategoryTanks.objects.filter(user = user).order_by('-date')
	data = data.order_by('-time')
	drinking_distance = []
	plant_distance = []
	bathing_distance = []
	car_distance = []
	date_time = []
	blank = ''
	for i in range(0,20):
		drinking_distance.append(data[i].drinkingWater_level)
		plant_distance.append(data[i].plantWater_level)
		car_distance.append(data[i].carWater_level)
		bathing_distance.append(data[i].bathingWater_level)
		if i==0 or i==19 or i==10:
			date_time.append(str(data[i].date))
		else:
			date_time.append(blank)
	context = {
		'date': date_time,
		'drinking_distance' : drinking_distance,
		'plant_distance' : plant_distance,
		'bathing_distance' : bathing_distance,
		'car_distance' : car_distance,
	}
	res = JsonResponse(context)
	res['Access-Control-Allow-Origin']="*"
	return res

@csrf_exempt
def getCurrentData(request):
	jsonResponse = json.loads(request.body.decode('utf-8'))
	email = jsonResponse['email']
	user = User.objects.get(email = email)
	data = CategoryTanks.objects.filter(user = user).order_by('-date')
	data = data.filter(date = data[0].date).order_by('-time')
	context = {
		'time' : data[0].time,
		'date' : data[0].date,
		'drinking_distance' : data[0].drinkingWater_level,
		'plant_distance' : data[0].plantWater_level,
		'bathing_distance' : data[0].bathingWater_level,
		'car_distance' : data[0].carWater_level
	}
	res = JsonResponse(context)
	res['Access-Control-Allow-Origin'] = "*"
	return res

@csrf_exempt
def controlActuator(request):
	print "ControlActuator WorkingHere"
	jsonResponse = json.loads(request.body.decode('utf-8'))
	email = jsonResponse['email']
	# email = request.user.UserProf.email
	user_profile = UserProfile.objects.get(email = email)
	actuator_link = user_profile.actuator_link

	value = int(jsonResponse['value'])
	# value = int(request.POST["value"])
	action = int(jsonResponse['action'])
	# action = request.POST["action"]
	print type(action), action, type(value), value, email
	# if action == 'true':
	# 	action = 1
	# else:
	# 	action = 0
	data = {'flag': action, 'actuator_id': value}
	try:
		res = requests.post(actuator_link, data=data)
		# print list(res)[:10]
		if value == 12 and action == 1:
			user_profile.drinkingWaterActuatorStatus = True
		elif value == 12 and action == 0:
			user_profile.drinkingWaterActuatorStatus = False
		if value == 16 and action == 1:
			user_profile.carWaterActuatorStatus = True
		elif value == 16 and action == 0:
			user_profile.carWaterActuatorStatus = False
		if value == 20 and action == 1:
			user_profile.bathingWaterActuatorStatus = True
		elif value == 20 and action == 0:
			user_profile.bathingWaterActuatorStatus = False
		if value == 26 and action == 1:
			user_profile.plantWaterActuatorStatus = True
		elif value == 26 and action == 0:
			user_profile.plantWaterActuatorStatus = False
		user_profile.save()
		context = { 'success' : 1 }
		res = JsonResponse(context)
		res['Access-Control-Allow-Origin'] = "*"
		return res
	except:
		context = { 'success' : 0 }
		res = JsonResponse(context)
		res['Access-Control-Allow-Origin'] = "*"
		return res

@csrf_exempt
def dataUpdate(request):
	print "Working Here"
	email = 'siddhant.k16@iiits.in'
	user = User.objects.get(email = email)
	data = CategoryTanks.objects.filter(user = user).order_by('-date')
	data = data.filter(date = data[0].date).order_by('-time')

	data1 = MainQuantumTank.objects.filter(user = user).order_by('-date')
	data1 = data1.filter(date = data1[0].date).order_by('-time')

	li = ["Drinking Water", "Car Water", "Bathing Water", "Plant Water"]
	type_of_water = li[int(data1[0].type_of_water)]

	user_profile = UserProfile.objects.get(email = email)
	context = {
		'time' : data[0].time,
		'date' : data[0].date,
		'drinking_distance' : data[0].drinkingWater_level,
		'plant_distance' : data[0].plantWater_level,
		'bathing_distance' : data[0].bathingWater_level,
		'car_distance' : data[0].carWater_level,
		'temperature' : data1[0].temperature,
		'humidity' : data1[0].humidity,
		'turbidity' : data1[0].turbidity,
		'pH' : data1[0].pH,
		'type_of_water': type_of_water,
		'actuator_control': user_profile.actuator_control,
		'actuator_link': user_profile.actuator_link,
		'drinkingWaterActuatorStatus': user_profile.drinkingWaterActuatorStatus,
		'carWaterActuatorStatus': user_profile.carWaterActuatorStatus,
		'bathingWaterActuatorStatus': user_profile.bathingWaterActuatorStatus,
		'plantWaterActuatorStatus': user_profile.plantWaterActuatorStatus
	}
	res = JsonResponse(context)
	return res

@csrf_exempt
def changeActuatorStatus(request):
	print "go for changeActuatorStatus"
	jsonResponse = json.loads(request.body.decode('utf-8'))
	email = jsonResponse['email']
	value = jsonResponse['value']
	print value,email
	cursor = connection.cursor()
	query = "UPDATE users_userprofile SET actuator_control = %d WHERE email = '%s'"%(int(value), email)
	cursor.execute(query)
	context = {
		'success' : 1,
		'error' : 0,
	}
	res = JsonResponse(context)
	res['Access-Control-Allow-Origin']="*"
	return res
