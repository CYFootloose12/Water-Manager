from django.db import models
from decimal import Decimal

# User class for built-in authentication module
from django.contrib.auth.models import User

class UserInfo(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	username = models.CharField(max_length=20)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.CharField(blank = True, max_length=32)
 	def __unicode__(self):
 		return 'UserInfo(id=' + str(self.id) + ')'

class Plant(models.Model):
	userInfo = models.ForeignKey(UserInfo)
	name = models.CharField(max_length=30)
	zip_code = models.CharField(max_length=5)
	type = models.CharField(max_length=30)
	def __unicode__(self):
		return 'Plant(id=' + str(self.id) + ')'

class WateringTime(models.Model):
	plant = models.ForeignKey(Plant)
	month = models.IntegerField()
	day = models.IntegerField()
	year = models.IntegerField()
	userAdded = models.BooleanField()
 	def __unicode__(self):
 		return '{"plant" : ' + str(self.plant.id) + ', "month" : ' + str(self.month) + ', "day" : ' + str(self.day) + ', "year" : ' + str(self.year) + ' "userAdded" :' + str(self.userAdded) + ' }'

class DayForecast(models.Model):
	plant = models.ForeignKey(Plant)
	month = models.IntegerField()
	day = models.IntegerField()
	year = models.IntegerField()
	high = models.IntegerField()
	low = models.IntegerField()
	total_precipitation = models.DecimalField(max_digits=5, decimal_places=2)
	humidity = models.IntegerField()
	def __unicode__(self):
		return 'Forecast(id=' + str(self.id) + ')'

