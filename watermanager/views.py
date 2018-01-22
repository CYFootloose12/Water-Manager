from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from watermanager.models import *
from watermanager.forms import RegistrationForm, EditForm, PlantForm
from django.contrib.auth import login, authenticate
from django.db import transaction
from django.http import HttpResponse, Http404
from django.template import loader, Context
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


from datetime import datetime

import time, datetime
import json

@login_required
def homeLogin(request):
    errors = []
    context = {}
    context['errors'] = errors
    errors = []
    userInfo = UserInfo.objects.filter(user=request.user)[0]
    plants = Plant.objects.filter(userInfo=userInfo)
    numPlants = ""
    for i in range(5-len(plants)):
        numPlants += "x"
    context = {'userInfo': userInfo, 'errors': errors, 'plants': plants, 'numPlants': numPlants}
    return render(request, 'watermanager/myplants.html', context)

@login_required
def index(request):
    errors = []
    if request.method == 'GET':
        context = {}
        context['form'] = RegistrationForm()
        return render(request, 'watermanager/index.html', context)
    context['errors'] = errors
    return render(request, 'watermanager/index.html')

@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'watermanager/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'watermanager/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'])
    new_user.is_active = False
    new_user.save()

    userInfo = UserInfo(user=new_user,
                    username=new_user.username,
                    first_name = new_user.first_name,
                    last_name = new_user.last_name,
                    email = new_user.email)
    userInfo.save()

    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to the Water Manager.  Please click the link below to
verify your email address and complete the registration of your account:
  http://%s%s
""" % (request.get_host(), 
       reverse('confirm', args=(new_user.username, token)))
    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="kevinzhu@andrew.cmu.edu",
              recipient_list=[new_user.email])
    context['email'] = form.cleaned_data['email']
    return render(request, 'watermanager/needs-confirmation.html', context)

@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'watermanager/confirmed.html', {})

@login_required
def myplants(request):
    errors = []
    print "yeasdf"
    userInfo = UserInfo.objects.filter(user=request.user)[0]
    plants = Plant.objects.filter(userInfo=userInfo)
    numPlants = ""
    for i in range(5-len(plants)):
        numPlants += "x"
    context = {'userInfo': userInfo, 'errors': errors, 'plants': plants, 'numPlants': numPlants }
    return render(request, 'watermanager/myplants.html', context)

@login_required
def add_plant(request):
    errors = []
    context = {}
    userInfo = UserInfo.objects.filter(user=request.user)[0]
    userInfoPlants = Plant.objects.filter(userInfo=userInfo)
    numPlants = ""
    if (len(userInfoPlants) < 5):
        if request.method == 'GET':
            context = { 'form': PlantForm() }
            return render(request, 'watermanager/add_plant.html', context)
        plant = Plant()
        plant_form = PlantForm(request.POST, instance=plant)
        if not plant_form.is_valid():
            context = { 'form': plant_form }
            return render(request, 'watermanager/add_plant.html', context)
        plant.userInfo = userInfo
        plant.save()
        # Save the new record
        plant_form.save()
        message = 'Plant created'
        edit_form = EditForm(instance=plant)
        plants = Plant.objects.filter(userInfo=userInfo)
        for i in range(5-len(plants)):
            numPlants += "x"
        context = {'userInfo': userInfo, 'plants': plants, 'numPlants': numPlants, 'errors' : errors }
        return render(request, 'watermanager/myplants.html', context)

    else:
        errors.append("Sorry, but you can only have five plants at one time.")
        context = {'userInfo' : userInfo, 'plants' : userInfoPlants, 'numPlants' : numPlants, 'errors' : errors }
        return render(request, 'watermanager/myplants.html', context)

@login_required
def delete_plant(request, plantID):
    errors = []
    try:
        plantID = int(plantID)
        userInfo = UserInfo.objects.filter(user=request.user)[0]
        plant_to_delete = Plant.objects.filter(id=plantID, userInfo=userInfo)[0]
        plant_to_delete.delete()
    except:
        errors.append("This plant does not exist, or you do not have permission to delete this plant.")

    plants = Plant.objects.filter(userInfo=userInfo)
    numPlants = ""
    for i in range(5-len(plants)):
        numPlants += "x"
    context = { 'userInfo' : userInfo, 'plants' : plants, 'numPlants' : numPlants, 'errors': errors}
    return render(request, 'watermanager/myplants.html', context)


@login_required
def schedule(request, plantID):
    context = {}
    errors = []
    userInfo = UserInfo.objects.filter(user=request.user)[0]
    plantID = int(plantID)
    try:
        plant = Plant.objects.get(id=plantID)
    #If the user does not, display a page not found error
    except Plant.DoesNotExist:
        raise Http404("The plant that you are looking for does not exist.")


    context = {'userInfo': userInfo, 'plant' : plant, 'errors': errors}

    return render(request, 'watermanager/schedule.html', context)

def add_events(request):
    plantID = request.GET['plantID']
    plantID = int(plantID)
    events = []
    plant = Plant.objects.get(id=plantID)
    wateringTimes = WateringTime.objects.filter(plant=plant)
    for wateringTime in wateringTimes:
        watering = {}
        watering['year'] = wateringTime.year
        watering['day'] = wateringTime.day
        watering['month'] = wateringTime.month
        watering['userAdded'] = wateringTime.userAdded
        events.append(watering)

    response_text=json.dumps(events)
    return HttpResponse(response_text)

def add_AI(request):
    plantID = request.GET.get('plantID', '')
    dayToday = request.GET.get('dayToday', '')
    monthToday = request.GET.get('monthToday', '')
    yearToday = request.GET.get('yearToday', '')

    plant = Plant.objects.filter(id=plantID)[0]

    #This is the score that determines if a given plant should be watered on a particular day.
    dayScore = 0

    #The amount of watering is based on the plant's type. For example, a cactus does not need as much water as a violet.
    typeFactor = 0
    
    lowWateringPlants = ['Cactus', 'Aloe Vera']
    lowMediumWateringPlants = ['Fern', 'Mint', 'Oregano', 'Sunflower', 'Garden Sage', 'Rosemary']
    highMediumWateringPlants = ['Snake Plant', 'Lavendar', 'Spider Plant', 'Daisy' ]
    highWateringPlants = ['Rose', 'Orchid', 'Petunia', 'Violet']
    if plant.type in lowWateringPlants:
        typeFactor = 0.2
    elif plant.type in lowMediumWateringPlants:
        typeFactor = 0.4
    elif plant.type in highMediumWateringPlants:
        typeFactor = 0.6
    elif plant.type in highWateringPlants:
        typeFactor = 0.8

    dayScore += typeFactor

    forecast = DayForecast.objects.filter(plant=plant)

    todayForecast = DayForecast.objects.filter(plant=plant, day=dayToday, month=monthToday, year=yearToday)[0]

    forecasts = []

    chosenForecasts = []

    numberOfForecasts = min(10, todayForecast.id);

    for i in range(todayForecast.id, numberOfForecasts+todayForecast.id):
        forecast = DayForecast.objects.filter(id=i)[0]
        forecasts.append(forecast)

    newWateringTimes = []

    for plantForecast in forecasts:
        
        #The amount of expected rain the plant receives determines when we will water the plant    
        rainFactor = 0

        #The amount of humidity plays a role in the amount of water that a plant should receive. The higher the humidity, the less evaporation 
        #that will occur and the less water the plant needs.

        humidityFactor = 0

        totalRain = plantForecast.total_precipitation
        if (totalRain < 0.05):
            rainFactor = 0.5
        
        elif (totalRain < 0.1):
            rainFactor = 0.3
        
        elif (totalRain < 0.2):
            rainFactor = 0.1
        

        totalHumidity = plantForecast.humidity
        if (totalHumidity < 30):
            humidityFactor = 0.4
           
        elif (totalHumidity < 45) :
            humidityFactor = 0.2
        
        elif (totalHumidity < 55):
            humidityFactor = 0.1
        

        #Factor of dayScore that is based on how often the plant has been watered in a given time span (3 days)
        scheduleFactor = 1.0

        dayBeforeForecastID = plantForecast.id - 1
        dayBeforeForecasts = DayForecast.objects.filter(id=dayBeforeForecastID)
        if (len(dayBeforeForecasts) > 0):
            dayBeforeForecast = dayBeforeForecasts[0]
            dayBeforeWateringTimes = WateringTime.objects.filter(month=dayBeforeForecast.month, day=dayBeforeForecast.day, year=dayBeforeForecast.year)

            #The plant has already been watered the day before
            if (len(dayBeforeWateringTimes) > 0):
                for i in range(0, len(dayBeforeWateringTimes)):
                    scheduleFactor -= 0.1
        
        forecastsOfDay = DayForecast.objects.filter(id=plantForecast.id)
        if (len(forecastsOfDay) > 0):
            dayOfForecast = forecastsOfDay[0]
            dayOfWateringTimes = WateringTime.objects.filter(month=dayOfForecast.month, day=dayOfForecast.day, year=dayOfForecast.year)

            #The plant is already being watered today
            if (len(dayOfWateringTimes) > 0):
                for i in range(0, len(dayOfWateringTimes)):
                    scheduleFactor -= 0.3

        dayAfterForecastID = plantForecast.id + 1
        dayAfterForecasts = DayForecast.objects.filter(id=dayAfterForecastID)
        if (len(dayAfterForecasts) > 0):
            dayAfterForecast = dayAfterForecasts[0]
            dayAfterWateringTimes = WateringTime.objects.filter(month=dayAfterForecast.month, day=dayAfterForecast.day, year=dayAfterForecast.year)

            #The plant is being watered tomorrow
            if (len(dayAfterWateringTimes) > 0):
                for i in range(0, len(dayAfterWateringTimes)):
                    scheduleFactor -= 0.1

        dayScore = typeFactor + rainFactor + humidityFactor + scheduleFactor

        #If the score is large enough, then a wateringTime will be put on that particular day,
        if (dayScore > 1.25):
            day = plantForecast.day
            print "Check this day aout"
            print day
            month = plantForecast.month
            year = plantForecast.year
            wateringTime = WateringTime(plant=plant, day=day, month=month, year=year, userAdded=False)
            wateringTime.save()
            watering = {}
            watering['year'] = wateringTime.year
            watering['day'] = wateringTime.day
            watering['month'] = wateringTime.month
            watering['userAdded'] = wateringTime.userAdded
            newWateringTimes.append(watering)
            chosenForecasts.append(plantForecast)


    response_text= json.dumps(newWateringTimes)
    print response_text
    return HttpResponse(response_text)


#Function that fetches data from an ajax request. The function receives different attributes of a particular forecast,
#and then stores it into the database.
def add_forecast(request):
    plantID = request.GET['plantID']
    month = request.GET.get('month')
    day = request.GET.get('day')
    year = request.GET.get('year')
    high = request.GET.get('high')
    low = request.GET.get('low')
    total_precipitation = request.GET.get('total_precipitation')
    humidity = request.GET.get('humidity')
    plant = Plant.objects.filter(id=plantID)[0]
    sameDayForecasts = DayForecast.objects.filter(plant=plant, month=month, day=day, year=year)
    if (len(sameDayForecasts) > 0):
        forecast = sameDayForecasts[0]
        forecast.high = high
        forecast.low = low 
        forecast.total_precipitation = total_precipitation
    else:
        dayForecast = DayForecast(plant=plant, month=month, day=day, year=year, high=high, low=low, total_precipitation=total_precipitation, humidity=humidity)
        dayForecast.save()
    return HttpResponse("")

#Function that receives data from an ajax request and stores the given information as a wateringTime
@login_required
def addWateringTime(request):

    plantID = request.GET['plantID']
    plant = Plant.objects.filter(id=plantID)[0]

    day = request.GET['day']
    month = request.GET['month']
    year = request.GET['year']

    #Retrieving the post that corresponds
    wateringTime = WateringTime(plant=plant, month=month, day=day, year=year, userAdded=True)
    wateringTime.save()
    response_text = ""
    return HttpResponse(response_text, content_type='text/html')

#Rendering of my_weather page
@login_required
def my_weather(request):
    context = {}
    userInfo = UserInfo(user=request.user)
    plants = Plant.objects.filter(userInfo=userInfo)
    context = { 'plants' : plants }
    return render(request, 'watermanager/my_weather.html', context)

#Rendering of the notifications page
@login_required
def notifications(request):
    context = {}
    userInfo = UserInfo(user=request.user)
    plants = Plant.objects.filter(userInfo=userInfo)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    daysOfTheWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    now = datetime.datetime.today()

    dayOfTheWeek = now.weekday()
    day = now.day
    month = now.month - 1 #January is the 0th month
    year = now.year    

    dates = []
    for i in range(0, len(daysOfTheWeek)):
        currentDate = now + datetime.timedelta(days=i)
        date = {}
        date['dayName'] = daysOfTheWeek[currentDate.weekday()]
        print date['dayName']
        date['monthName'] = months[currentDate.month-1]
        date['day'] = currentDate.day
        date['year'] = currentDate.year
        userWaterings = []
        for plant in plants:
            plantWatering = WateringTime.objects.filter(plant=plant, month=(currentDate.month-1), day=currentDate.day, year=currentDate.year)
            for watering in plantWatering:
                userWaterings.append(watering)

        date['wateringTimes'] = userWaterings
        dates.append(date)

    context = { 'dates' : dates }
    return render(request, 'watermanager/notifications.html', context)


@login_required
def send_email_notifications(request):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    daysOfTheWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    emailBody = str(request.user.first_name) + ", \n \n"
    emailBody += "Here are your waterings for the next week. \n \n"
    userInfo = UserInfo(user=request.user)
    plants = Plant.objects.filter(userInfo=userInfo)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    daysOfTheWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    now = datetime.datetime.today()

    dayOfTheWeek = now.weekday()
    day = now.day
    month = now.month - 1 #January is the 0th month
    year = now.year    

    dates = []
    for i in range(0, len(daysOfTheWeek)):
        currentDate = now + datetime.timedelta(days=i)
        date = {}
        date['dayName'] = daysOfTheWeek[currentDate.weekday()]
        date['monthName'] = months[currentDate.month-1]
        date['day'] = currentDate.day
        date['year'] = currentDate.year
        userWaterings = []
        for plant in plants:
            plantWatering = WateringTime.objects.filter(plant=plant, month=(currentDate.month-1), day=currentDate.day, year=currentDate.year)
            for watering in plantWatering:
                userWaterings.append(watering)

        date['wateringTimes'] = userWaterings
        dates.append(date)

    for date in dates:
        dateLine = str(date['dayName']) + ", " + str(date['monthName']) + " " + str(date['day']) + ", " + str(date['year']) + "\n"
        print dateLine
        emailBody += dateLine
        for watering in date['wateringTimes']:
            emailBody += "      -"
            emailBody += watering.plant.name + "\n"

    emailBody += "\nHope you enjoy your week! Happy plants, happy life!"
        
    send_mail(subject="Your Watering Times Email Notification",
              message= emailBody,
              from_email="support@watermanager.com",
              recipient_list=[request.user.email])

    message = "Great! An email notification with the list of the next week's waterings have been sent to your email."
    context = { 'emailBody' : emailBody, 'dates' : dates, 'message' : message }

    return render(request, 'watermanager/notifications.html', context)


#Function to delete a particular wateringTime
@login_required
def deleteWateringTime(request):

    plantID = request.GET['plantID']
    plant = Plant.objects.filter(id=plantID)[0]

    wateringDate = request.GET['date']
    wateringDate = str(wateringDate)
    dateParts = wateringDate.split()

    color = request.GET['color']
    month = dateParts[1]

    userAdded = ""

    dayNumber = int(dateParts[2])

    yearNumber = int(dateParts[3])

    abbreviatedMonths = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    monthNumber = abbreviatedMonths.index(month)

    if (color == 'red'):
        print "This is AI added."
        userAdded = False
    else:
        print "This is user added"
        userAdded = True

    wateringDate = WateringTime.objects.filter(plant=plant, day=dayNumber, month=monthNumber, year=yearNumber, userAdded=userAdded)
    wateringDate.delete()

    response_text = ''
    return HttpResponse(response_text, content_type='text/html')
