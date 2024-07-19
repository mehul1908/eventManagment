from django.db import models  
from datetime import datetime

from django.contrib.auth.models import AbstractUser
# Create your models here.

class Users(AbstractUser):
	age = models.IntegerField(default=18)
	address = models.CharField(max_length=50 , default='default')

class Event(models.Model):
	eventName = models.CharField(max_length=40)
	description = models.CharField(max_length=100)
	venue = models.CharField(max_length=100)
	type = models.CharField(max_length=30)
	time = models.DateTimeField(default = datetime.now)
	entryFee = models.FloatField()
	organizer_id = models.ForeignKey(Users , on_delete=models.CASCADE)
	def __str__(self):
		return str(self.id) + self.eventName
	
class Participant(models.Model):
	eventId = models.ForeignKey(Event ,on_delete=models.CASCADE)
	attendee = models.ForeignKey(Users ,on_delete=models.CASCADE)
	time = models.DateTimeField(default=datetime.now)
	pdfFile = models.FileField(upload_to='welcomeFile' , default='default.pdf')

	def __str__(self):
		return str(self.id)+'.' + str(self.attendee.id) +'.'+str(self.eventId.eventName)