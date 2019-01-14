from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from django.http import JsonResponse
import json, time, random
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core import serializers
from django.db.models.functions import Extract
from django.db.models import Avg, Count
import requests


def turnOnOffActuator(d, c, b, p, userprofile, actuator_link):
    l = [-1] * 4
    if d != -1:
        data = {'flag': d, 'actuator_id': 20}
        flag = True
        try:
            res = requests.post(actuator_link, data=data)
        except:
            flag = False

        if d == 1 and flag == True:
            userprofile.drinkingWaterActuatorStatus = True
        elif flag == True:
            userprofile.drinkingWaterActuatorStatus = False
        l[0] = str(flag)

    if c != -1:
        data = {'flag': c, 'actuator_id': 12}
        flag = True
        try:
            res = requests.post(actuator_link, data=data)
        except:
            flag = False
        if c == 1 and flag == True:
            userprofile.carWaterActuatorStatus = True
        elif flag == True:
            userprofile.carWaterActuatorStatus = False
        l[1] = str(flag)

    if b != -1:
        data = {'flag': b, 'actuator_id': 26}
        flag = True
        try:
            res = requests.post(actuator_link, data=data)
        except:
            flag = False
        if b == 1 and flag == True:
            userprofile.bathingWaterActuatorStatus = True
        elif flag == True:
            userprofile.bathingWaterActuatorStatus = False
        l[2] = str(flag)

    if p != -1:
        data = {'flag': p, 'actuator_id': 16}
        flag = True
        try:
            res = requests.post(actuator_link, data=data)
        except:
            flag = False
        if p == 1 and flag == True:
            userprofile.plantWaterActuatorStatus = True
        elif flag == True:
            userprofile.plantWaterActuatorStatus = False
        l[3] = str(flag)

    userprofile.save()

    return l


@method_decorator(csrf_exempt, name='dispatch')
class logQuantumMainTankData(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('THIS IS GET REQUEST TO LOGDATA OF QUNATUM AND MAIN TANKS')

    def post(self, request, *args, **kwargs):
        mobile_no = str(request.POST.get("mobile_no", ""))
        mainTank_level = float(request.POST.get("mainTank_level", ""))
        quantumTank_level = float(request.POST.get("quantumTank_level", ""))
        temperature = float(request.POST.get("temperature", ""))
        turbidity = float(request.POST.get("turbidity", ""))
        humidity = float(request.POST.get("humidity", ""))
        pH = float(request.POST.get("pH", ""))

        if turbidity < 5:
            type_of_water = 0
        elif turbidity >= 5 and turbidity <= 20:
            type_of_water = 2
        elif turbidity >= 20 and turbidity <= 40:
            type_of_water = 3
        else:
            type_of_water = 1

        user = User.objects.get(username=mobile_no)
        userprofile = UserProfile.objects.get(user=user)
        actuator_link = userprofile.actuator_link
        sensors_data = MainQuantumTank()
        sensors_data.user = user
        sensors_data.mainTank_level = ((float(userprofile.mainTank_capacity) - float(mainTank_level)) / float(
            userprofile.mainTank_capacity)) * 100
        sensors_data.quantumTank_level = ((float(userprofile.quantumTank_capacity) - float(quantumTank_level)) / float(
            userprofile.quantumTank_capacity)) * 100

        if userprofile.mainTank_capacity < mainTank_level:
            sensors_data.mainTank_level = 0

        if userprofile.quantumTank_capacity < quantumTank_level:
            sensors_data.quantumTank_level = 0

        sensors_data.temperature = float(temperature)
        sensors_data.turbidity = float(turbidity)
        sensors_data.humidity = float(humidity)
        sensors_data.date = time.strftime("%Y-%m-%d")
        sensors_data.time = time.strftime("%X")
        sensors_data.type_of_water = type_of_water
        sensors_data.pH = pH

        if int(userprofile.actuator_control) == 0:
            if sensors_data.quantumTank_level <= 10 or sensors_data.quantumTank_level >= 90:
                sensors_data.save()

                flag = [0, 0, 0, 0]

                print pH

                if (pH >= 6 and pH <= 8.2):
                    flag = [1, 0, 0, 0]
                elif (pH > 8.2 and pH <= 9) or (pH >= 5.2 and pH <= 6):
                    flag = [0, 0, 1, 0]
                elif (pH > 4 and pH <= 5.2) or (pH >= 9 and pH <= 10):
                    flag = [0, 0, 0, 1]
                elif (pH > 0 and pH <= 4) or (pH >= 10 and pH <= 14):
                    flag = [0, 1, 0, 0]

                if sensors_data.quantumTank_level <= 10:
                    flag = [0, 0, 0, 0]

                print flag

            l = turnOnOffActuator(flag[0], flag[1], flag[2], flag[3], userprofile, actuator_link)

        return HttpResponse('Done')


@method_decorator(csrf_exempt, name='dispatch')
class logCategoryTanksData(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('THIS IS GET REQUEST TO LOGDATA CATEGORY TANKS')

    def post(self, request, *args, **kwargs):
        mobile_no = str(request.POST.get("mobile_no", ""))
        drinkingWater_level = float(request.POST.get("drinkingWater_level", ""))
        carWater_level = float(request.POST.get("carWater_level", ""))
        plantWater_level = float(request.POST.get("plantWater_level", ""))
        bathingWater_level = float(request.POST.get("bathingWater_level", ""))
        user = User.objects.get(username=mobile_no)
        userprofile = UserProfile.objects.get(user=user)
        actuator_link = userprofile.actuator_link
        sensors_data = CategoryTanks()
        sensors_data.user = user
        sensors_data.drinkingWater_level = ((float(userprofile.drinkingWater_capacity) - float(
            drinkingWater_level)) / float(userprofile.drinkingWater_capacity)) * 100
        sensors_data.carWater_level = ((float(userprofile.carWater_capacity) - float(carWater_level)) / float(
            userprofile.carWater_capacity)) * 100
        sensors_data.bathingWater_level = ((float(userprofile.bathingWater_capacity) - float(
            bathingWater_level)) / float(userprofile.bathingWater_capacity)) * 100
        sensors_data.plantWater_level = ((float(userprofile.plantWater_capacity) - float(plantWater_level)) / float(
            userprofile.plantWater_capacity)) * 100
        if userprofile.drinkingWater_capacity < drinkingWater_level:
            sensors_data.drinkingWater_level = 0
        if userprofile.carWater_capacity < carWater_level:
            sensors_data.carWater_level = 0
        if userprofile.bathingWater_capacity < bathingWater_level:
            sensors_data.bathingWater_level = 0
        if userprofile.plantWater_capacity < plantWater_level:
            sensors_data.plantWater_level = 0
        print type(userprofile.actuator_control)
        if int(userprofile.actuator_control) == 0:
            flag = [-1, -1, -1, -1]
            if sensors_data.drinkingWater_level >= 60:
                flag[0] = 0
            else:
                flag[0] = -1
            if sensors_data.bathingWater_level >= 60:
                flag[2] = 0
            else:
                flag[2] = -1
            if sensors_data.plantWater_level >= 60:
                flag[3] = 0
            else:
                flag[3] = -1
            if sensors_data.carWater_level >= 60:
                flag[1] = 0
            else:
                flag[1] = -1
            print flag
            turnOnOffActuator(flag[0], flag[1], flag[2], flag[3], userprofile, actuator_link)
        sensors_data.date = time.strftime("%Y-%m-%d")
        sensors_data.time = time.strftime("%X")
        sensors_data.save()
        return HttpResponse('DONE')


def homepage(request):
    return render(request, 'users/homepage.html')


def Signup(request):
    if request.method == 'GET':
        return render(request, 'users/signup.html')
    if request.method == 'POST':
        user = User()
        user_prof = UserProfile()
        name = request.POST['name']
        password = request.POST['password']
        email = request.POST['email']
        mob_no = request.POST['mob_no']

        user.username = mob_no
        user.set_password(password)
        user.email = email
        user.save()

        user_prof.name = name
        user_prof.password = password  # Reference Purpose Only Nigga
        user_prof.mob_no = mob_no
        user_prof.email = email
        user_prof.user = user
        user_prof.save()

        return HttpResponse("user signed up")


def Login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return render(request, 'users/main.html')
        return render(request, 'users/login.html')
    if request.method == 'POST':
        mob_no = request.POST['mob_no'];
        password = request.POST['password']
        user_prof = get_object_or_404(UserProfile, mob_no=mob_no)
        user = authenticate(username=mob_no, password=password)
        print ("user is ", user)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('../main')
        else:
            return HttpResponse("Wrong Mobile Number Or Password")


@login_required(login_url='/users/login')
def Main(request):
    if request.method == 'GET':
        query = "SELECT * FROM users_userprofile WHERE email='%s'" % (request.user.UserProf.email)
        data = UserProfile.objects.raw(query)
        return render(request, 'users/main.html')


def home(request):
    email = request.user.UserProf.email
    print(email)
    user = User.objects.get(email=email, is_superuser=False)
    userprofile = UserProfile.objects.get(user=user)
    return render(request, 'users/home.html', {'mobile': userprofile.mob_no})


def dataUpdate(request, mobile_no):
    user1 = User.objects.get(username=mobile_no)
    email = user1.email
    user = User.objects.get(email=email)
    data = CategoryTanks.objects.filter(user=user).order_by('-date')
    data = data.filter(date=data[0].date).order_by('-time')

    data1 = MainQuantumTank.objects.filter(user=user).order_by('-date')
    data1 = data1.filter(date=data1[0].date).order_by('-time')

    li = ["Drinking Water", "Car Water", "Bathing Water", "Plant Water"]
    type_of_water = li[int(data1[0].type_of_water)]

    user_profile = UserProfile.objects.get(email=email)
    context = {
        'time': data[0].time,
        'date': data[0].date,
        'drinking_distance': data[0].drinkingWater_level,
        'plant_distance': data[0].plantWater_level,
        'bathing_distance': data[0].bathingWater_level,
        'car_distance': data[0].carWater_level,
        'temperature': data1[0].temperature,
        'humidity': data1[0].humidity,
        'turbidity': data1[0].turbidity,
        'pH': data1[0].pH,
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


def Dashboard(request):
    date = time.strftime("%Y-%m-%d");
    return render(request, 'users/dashboard.html', {"date": date})


def Residence(request):
    return render(request, 'users/residenceSettings.html')


def GetInitialSettingsDetails(request):
    if request.method == 'POST':
        query = "SELECT * FROM users_userprofile WHERE email='%s'" % (request.user.UserProf.email)
        data = UserProfile.objects.raw(query)
        context = {
            'name': data[0].name,
            'mob_no': data[0].mob_no,
            'email': data[0].email,
            'address': data[0].address,
            'city': data[0].city,
            'pincode': data[0].pincode,
            'vehicles': data[0].vehicles,
            'members': data[0].members,
            'plants': data[0].plants,
            'mainTank_capacity': data[0].mainTank_capacity,
            'carWater_capacity': data[0].carWater_capacity,
            'drinkingWater_capacity': data[0].drinkingWater_capacity,
            'bathingWater_capacity': data[0].bathingWater_capacity,
            'plantWater_capacity': data[0].plantWater_capacity,
            'actuator_control': data[0].actuator_control,
            'actuator_link': data[0].actuator_link,
            'success': 1,
            'error': 0,
        }
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin'] = "*"
        return res


def UpdateResidenceDetails(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        query = "UPDATE users_userprofile SET address = '%s', city = '%s', pincode = %d WHERE email = '%s'" % (
        request.POST["address"], request.POST["city"], int(request.POST["pincode"]), request.user.UserProf.email)
        cursor.execute(query)
        context = {
            'success': 1,
            'error': 0,
        }
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin'] = "*"
        return res


def UpdateVehicles(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        query = "UPDATE users_userprofile SET vehicles = %d WHERE email = '%s'" % (
        int(request.POST["vehicleNum"]), request.user.UserProf.email)
        cursor.execute(query)
        context = {
            'success': 1,
            'error': 0,
        }
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin'] = "*"
        return res


def UpdateMembers(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        query = "UPDATE users_userprofile SET members = %d WHERE email = '%s'" % (
        int(request.POST["memberNum"]), request.user.UserProf.email)
        cursor.execute(query)
        context = {
            'success': 1,
            'error': 0,
        }
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin'] = "*"
        return res


def UpdatePlants(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        query = "UPDATE users_userprofile SET plants = %d WHERE email = '%s'" % (
        int(request.POST["plantNum"]), request.user.UserProf.email)
        cursor.execute(query)
        context = {
            'success': 1,
            'error': 0,
        }
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin'] = "*"
        return res


def updateActuatorControlSettings(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        query = "UPDATE users_userprofile SET actuator_control = %d WHERE email = '%s'" % (
        int(request.POST["value"]), request.user.UserProf.email)
        cursor.execute(query)
        context = {
            'success': 1,
            'error': 0,
        }
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin'] = "*"
        return res


def updateReservoirSettings(request):
    if request.method == 'POST':
        cursor = connection.cursor()
        query = "UPDATE users_userprofile SET mainTank_capacity = %d, drinkingWater_capacity = %d, carWater_capacity = %d, bathingWater_capacity = %d, plantWater_capacity = %d WHERE email = '%s'" % (
        int(request.POST["mainTank"]), int(request.POST["drinkingWater"]), int(request.POST["carWater"]),
        int(request.POST["bathingWater"]), int(request.POST["plantWater"]), request.user.UserProf.email)
        cursor.execute(query)
        context = {
            'success': 1,
            'error': 0,
        }
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin'] = "*"
        return res


def updateActuatorLinkSettings(request):
    if request.method == 'POST':
        user = UserProfile.objects.get(email=request.user.UserProf.email)
        user.actuator_link = request.POST["link"]
        user.save()
        context = {
            'success': 1,
            'error': 0,
        }
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin'] = "*"
        return res


def showDataDateRange(request):
    if request.is_ajax():
        start_date = request.POST.get('start_date', None)
        end_date = request.POST.get('end_date', None)
        user = get_object_or_404(User, email=request.user.UserProf.email, is_superuser=False)
        category_time_array = []
        mainQunatum_time_array = []
        drinkingWater_level_array = []
        plantWater_level_array = []
        carWater_level_array = []
        bathingWater_level_array = []
        mainTank_level_array = []
        quantumTank_level_array = []
        tow = []
        if start_date == end_date:
            data = CategoryTanks.objects.filter(date__range=(start_date, end_date), user=user)
            for obj in data:
                category_time_array.append(obj.time)
                drinkingWater_level_array.append(obj.drinkingWater_level)
                bathingWater_level_array.append(obj.bathingWater_level)
                carWater_level_array.append(obj.carWater_level)
                plantWater_level_array.append(obj.plantWater_level)
            data = MainQuantumTank.objects.filter(date__range=(start_date, end_date), user=user)
            for obj in data:
                mainQunatum_time_array.append(obj.time)
                mainTank_level_array.append(obj.mainTank_level)
                quantumTank_level_array.append(obj.quantumTank_level)
            type_of_water = data.values('type_of_water').annotate(Count('type_of_water'))
            print type_of_water
            for obj in type_of_water:
                tow.append(obj["type_of_water__count"])
        else:
            data = CategoryTanks.objects.filter(date__range=(start_date, end_date), user=user)
            data = data.values('date').annotate(Avg('drinkingWater_level'), Avg('carWater_level'),
                                                Avg('bathingWater_level'), Avg('plantWater_level'))
            for obj in data:
                category_time_array.append(obj["date"])
                plantWater_level_array.append(obj["plantWater_level__avg"])
                carWater_level_array.append(obj["carWater_level__avg"])
                bathingWater_level_array.append(obj["bathingWater_level__avg"])
                drinkingWater_level_array.append(obj["drinkingWater_level__avg"])
            data = MainQuantumTank.objects.filter(date__range=(start_date, end_date), user=user)
            data1 = data.values('date').annotate(Avg('mainTank_level'), Avg('quantumTank_level'))
            for obj in data1:
                mainQunatum_time_array.append(obj["date"])
                mainTank_level_array.append(obj["mainTank_level__avg"])
                quantumTank_level_array.append(obj["quantumTank_level__avg"])
            type_of_water = data.values('type_of_water').annotate(Count('type_of_water'))
            print type_of_water
            for obj in type_of_water:
                tow.append(obj["type_of_water__count"])
        context = {
            'category_time': category_time_array,
            'mainQuantum_time': mainQunatum_time_array,
            'plantWater': plantWater_level_array,
            'carWater': carWater_level_array,
            'bathingWater': bathingWater_level_array,
            'drinkingWater': drinkingWater_level_array,
            'mainTank': mainTank_level_array,
            'quantumTank': quantumTank_level_array,
            'type_of_water': tow,
        }
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin'] = "*"
        return res


def predictions(request):
    return render(request, 'users/predictions.html')


def predictionsData(request):
    email = request.user.UserProf.email
    userProfile = User.objects.get(email=email)
    data = MainQuantumTank.objects.filter(user=userProfile)
    data1 = data.order_by('date')
    data1 = data1.values('date').annotate(Count('date'))
    no_of_dates = len(data1)
    obj = data.values('type_of_water').annotate(Count('type_of_water'))
    drinkingWater_level_avg = float(obj[0]["type_of_water__count"]) / no_of_dates
    carWater_level_avg = float(obj[1]["type_of_water__count"]) / no_of_dates
    bathingWater_level_avg = float(obj[2]["type_of_water__count"]) / no_of_dates
    plantWater_level_avg = float(obj[3]["type_of_water__count"]) / no_of_dates
    print obj[0]["type_of_water__count"], obj[1]["type_of_water__count"], obj[2]["type_of_water__count"], obj[3][
        "type_of_water__count"]
    context = [round(drinkingWater_level_avg, 2), round(carWater_level_avg, 2), round(bathingWater_level_avg, 2),
               round(plantWater_level_avg, 2)]
    print context
    context = {'data': context}
    res = JsonResponse(context)
    res['Access-Control-Allow-Origin'] = "*"
    return res


@csrf_exempt
def controlActuator(request):
    email = request.user.UserProf.email
    user_profile = UserProfile.objects.get(email=email)
    actuator_link = user_profile.actuator_link
    value = int(request.POST["value"])
    action = request.POST["action"]
    print type(action)
    if action == 'true':
        action = 1
    else:
        action = 0
    data = {'flag': action, 'actuator_id': value}
    try:
        res = requests.post(actuator_link, data=data)
        print res

        if value == 20 and action == 1:
            user_profile.drinkingWaterActuatorStatus = True
        elif value == 20 and action == 0:
            user_profile.drinkingWaterActuatorStatus = False

        if value == 12 and action == 1:
            user_profile.carWaterActuatorStatus = True
        elif value == 12 and action == 0:
            user_profile.carWaterActuatorStatus = False

        if value == 26 and action == 1:
            user_profile.bathingWaterActuatorStatus = True
        elif value == 26 and action == 0:
            user_profile.bathingWaterActuatorStatus = False

        if value == 16 and action == 1:
            user_profile.plantWaterActuatorStatus = True
        elif value == 16 and action == 0:
            user_profile.plantWaterActuatorStatus = False

        user_profile.save()
        context = {'success': 1}
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin'] = "*"
        return res
    except:
        context = {'success': 0}
        res = JsonResponse(context)
        res['Access-Control-Allow-Origin'] = "*"
        return res


def city(request, cityID):
    city = ['Jaipur', 'Chennai', 'Delhi', 'Mumbai', 'Klkata', 'Hyderabad', 'Banglore', 'Pune']
    return render(request, 'users/city.html', {'cityID': cityID, 'cityName': city[int(cityID)]})


def cityData(request):
    cityID = request.POST["cityID"]
    users = UserProfile.objects.filter(city=cityID)
    total_d_avg = 0
    total_c_avg = 0
    total_b_avg = 0
    total_p_avg = 0
    for u in users:
        userProfile = User.objects.get(email=u.email)
        data = MainQuantumTank.objects.filter(user=userProfile)
        data1 = data.order_by('date')
        data1 = data1.values('date').annotate(Count('date'))
        no_of_dates = len(data1)
        obj = data.values('type_of_water').annotate(Count('type_of_water'))

        drinkingWater_level_avg = 0
        carWater_level_avg = 0
        bathingWater_level_avg = 0
        plantWater_level_avg = 0
        if len(data1) > 0:
            drinkingWater_level_avg = float(obj[0]["type_of_water__count"]) / no_of_dates
            carWater_level_avg = float(obj[1]["type_of_water__count"]) / no_of_dates
            bathingWater_level_avg = float(obj[2]["type_of_water__count"]) / no_of_dates
            plantWater_level_avg = float(obj[3]["type_of_water__count"]) / no_of_dates

        total_d_avg += drinkingWater_level_avg
        total_c_avg += carWater_level_avg
        total_b_avg += bathingWater_level_avg
        total_p_avg += plantWater_level_avg

    total_d_avg /= len(users)
    total_c_avg /= len(users)
    total_b_avg /= len(users)
    total_p_avg /= len(users)

    context = [round(total_d_avg, 2), round(total_c_avg, 2), round(total_b_avg, 2), round(total_p_avg, 2)]
    context = {'data': context, 'noOfUsers': len(users)}
    res = JsonResponse(context)
    res['Access-Control-Allow-Origin'] = "*"
    return res
