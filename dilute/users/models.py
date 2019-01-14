from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import time


class UserProfile(models.Model):
	CITY_CHOICES = (
		('0', 'Jaipur'),
		('1', 'Chennai'),
		('2', 'Delhi'),
		('3', 'Mumbai'),
		('4', 'Kolkata'),
		('5', 'Hyderabad'),
		('6', 'Banglore'),
		('7', 'Pune')
		)

	ACTUATOR_CONTROL_CHOICES = (
		('0', 'Automatic'),
		('1', 'Manual'),
		)

	name = models.CharField(max_length=20, null=True, blank=True, default="test_name")
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='UserProf')
	mob_no = models.CharField(max_length=13, null=False, default=None, unique=True)
	password = models.CharField(max_length=20, null=True, blank=True, default=None)
	email = models.CharField(max_length=40, null=False)
	address = models.CharField(max_length = 60, null = True, default = "")
	city = models.CharField(max_length = 50, choices = CITY_CHOICES, default = "Chennai")
	pincode = models.CharField(max_length = 10, default = "", null = True)
	vehicles = models.IntegerField(default = 0, null = True)
	members = models.IntegerField(default = 0, null = True)
	plants = models.IntegerField(default = 0, null = True)

	mainTank_capacity = models.FloatField(null=True, default=100, blank=True)
	quantumTank_capacity = models.FloatField(null=True, default=100, blank=True)
	drinkingWater_capacity = models.FloatField(null=True, default=100, blank=True)
	carWater_capacity = models.FloatField(null=True, default=100, blank=True)
	bathingWater_capacity = models.FloatField(null=True, default=100, blank=True)
	plantWater_capacity = models.FloatField(null=True, default=100, blank=True)

	actuator_control = models.CharField(max_length = 10, choices = ACTUATOR_CONTROL_CHOICES, default=0)
	actuator_link = models.CharField(max_length=200, blank=True)

	drinkingWaterActuatorStatus = models.BooleanField(default = False)
	carWaterActuatorStatus = models.BooleanField(default = False)
	bathingWaterActuatorStatus = models.BooleanField(default = False)
	plantWaterActuatorStatus = models.BooleanField(default = False)

	def __str__(self):
		return (str(self.user.username))

class MainQuantumTank(models.Model):
	WATER_TYPE_CHOICES = (
		('0', 'drinkingWater'),
		('1', 'carwater'),
		('2', 'bathingwater'),
		('3', 'plantwater')
		)

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="MainQuantumTank")

	mainTank_level = models.FloatField(null=True, default=0, blank=True)
	quantumTank_level = models.FloatField(null=True, default=0, blank=True)

	temperature = models.FloatField(null=True, blank=True, default=30)
	turbidity = models.FloatField(null=True, blank=True)
	humidity = models.FloatField(null=True, blank=True)
	pH = models.FloatField(null=True, blank=True)

	date = models.DateField(null=True, blank=True, default=time.strftime("%Y-%m-%d"))
	time = models.TimeField(null=True, default=time.strftime("%X"))

	type_of_water = models.CharField(max_length=50, choices=WATER_TYPE_CHOICES, null=True, blank=True)

	def __str__(self):
		return str(self.user.username) + " --> " + str(self.date) + " --> " + str(self.time)

class CategoryTanks(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="CategoryTanks")
	drinkingWater_level = models.FloatField(null=True, default=0, blank=True)
	carWater_level = models.FloatField(null=True, default=0, blank=True)
	bathingWater_level = models.FloatField(null=True, default=0, blank=True)
	plantWater_level = models.FloatField(null=True, default=0, blank=True)

	date = models.DateField(null=True, blank=True, default=time.strftime("%Y-%m-%d"))
	time = models.TimeField(null=True, default=time.strftime("%X"))

	def __str__(self):
		return str(self.user.username) + " --> " + str(self.date) + " --> " + str(self.time)