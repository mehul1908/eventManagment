from . import models
from rest_framework import serializers  # type: ignore
from django import forms

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Users
		exclude = ["last_login" ,"date_joined" , "groups" , "user_permissions"]

class EventSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Event
		fields="__all__"

class ParticipantSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Participant
		fields="__all__"

