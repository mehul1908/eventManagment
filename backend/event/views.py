from rest_framework.response import Response 
from rest_framework.views import APIView 
from rest_framework import status
from . import models ,serializer
from django.http import HttpResponse
from django.contrib import auth  
from django.db.models import Q
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
from django.core.mail import EmailMessage


def changeUser(request , user):
	return  user.username == request.user.username

def home(request):
	
	return HttpResponse("Hello world")


#User API Views...........................................

class UserListView(APIView):
	def get(self , request):
		users = models.Users.objects.all()
		ser = serializer.UserSerializer(users , many = True)
		return Response(ser.data , status.HTTP_200_OK)
	
	def post(self , request):
		ser = serializer.UserSerializer(data= request.data)
		if ser.is_valid():
			ser.save()
			demo = models.Users.objects.get(username=request.data["username"])
			demo.set_password(request.data["password"])
			demo.save()
			return Response(ser.data , status.HTTP_201_CREATED)
		return Response(ser.errors , status.HTTP_406_NOT_ACCEPTABLE)

def loginUser(request , username , password):
	user = auth.authenticate(username = username , password = password)
	if user is not None:
		auth.login(request , user)
	return user
	
def logoutUser(request):
	auth.logout(request)
	return Response(status=status.HTTP_200_OK)

class UserDetailView(APIView):
	def getUser(self , id):
		try:
			return models.Users.objects.get(username = id)
		except:
			return None
		
	
	def get(self , request , id , password=None):
		if password:
			user = loginUser(request , id , password)
			ser = serializer.UserSerializer(user)
		
			if user is not None:
				if not(user.is_active):
					return({'message':'User is inactive'} , status.HTTP_406_NOT_ACCEPTABLE)
				else:
					return Response(ser.data , status.HTTP_202_ACCEPTED)
			
			else:
				return Response(ser.data ,status=status.HTTP_401_UNAUTHORIZED)
		else :
			user = self.getUser(id)
			
			if user is None:
				return Response(status=status.HTTP_404_NOT_FOUND)
			ser = serializer.UserSerializer(user)
			return Response(ser.data , status.HTTP_200_OK)
	
	def put(self , request , id):
		user = self.getUser(id)
		
		if user is None:
				return Response(status=status.HTTP_404_NOT_FOUND)
		
		ser = serializer.UserSerializer(user , request.data)
		if ser.is_valid():
			ser.save()
			user.set_password(request.data["password"])
			user.save()	
			return Response(ser.data , status = status.HTTP_202_ACCEPTED)
		return Response(ser.errors , status = status.HTTP_400_BAD_REQUEST)
	
	def delete(self , request , id):
		user = self.getUser(id)
		if user is None:
				return Response(status=status.HTTP_404_NOT_FOUND)
		user.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class GetInActiveUser(APIView):
	def get(self , request):
		users = models.Users.objects.filter(is_active = False)
		ser = serializer.UserSerializer(users , many = True)
		return Response(ser.data , status.HTTP_200_OK)

class MakeActiveUser(APIView):
	def get(self , request , ids):
		arr = ids.split('-')
		for id in arr:
			user = models.Users.objects.get(pk = id)
			user.is_active = True
			user.save()
		return Response(status=status.HTTP_202_ACCEPTED)


#Event API Views.................................
class EventListView(APIView):
	def get(self , request , attribute=None , keyword=None):
		loginUser = request.user
		events = models.Event.objects.all()
		if loginUser.is_staff == True and loginUser.is_superuser == False :
			events = events.filter(organizer_id = loginUser.username)
		if attribute == 'organizer_id' :
			events = events | events.filter(organizer_id__contains = int(keyword))
		if attribute == 'type' :
			events = events | events.filter(type__contains = keyword)
		if attribute == 'eventName' :
			events = events | events.filter(eventName__contains = keyword)
		if attribute == 'venue' :
			events = events | events.filter(venue__contains = keyword)
		ser = serializer.EventSerializer(events , many=True)
		return Response(ser.data , status.HTTP_200_OK)
	def post(self , request):
		ser = serializer.EventSerializer(data = request.data)
		if ser.is_valid():
			ser.save()
			
			return Response(ser.data , status.HTTP_201_CREATED)
		return Response(ser.errors , status.HTTP_406_NOT_ACCEPTABLE)


class EventDetailView(APIView):
	def getEvent(self , pk):
		try:
			event = models.Event.objects.get(pk =pk )
			return event
		except:
			return None
	
	def get(self , request , pk):
		event = self.getEvent(pk)
		if event is None:
				return Response(status=status.HTTP_404_NOT_FOUND)
		ser = serializer.EventSerializer(event)
		return Response(ser.data , status=status.HTTP_200_OK)
	
	def put(self , request , pk):
		event = self.getEvent(pk)
		if event is None:
				return Response(status=status.HTTP_404_NOT_FOUND)
		ser = serializer.EventSerializer(event , request.data)
		if ser.is_valid():
			
			ser.save()
			return Response(ser.data,status=status.HTTP_202_ACCEPTED)
		return Response(ser.errors , status.HTTP_400_BAD_REQUEST)
	
	def delete(self , request , pk):
		event = self.getEvent(pk)
		if event is None:
				return Response(status=status.HTTP_404_NOT_FOUND)
		event.delete()
		return Response(status=status.HTTP_205_RESET_CONTENT)


#For Participants

class ParticipantsListView(APIView):
	def get(self , request , keyword = None):
		if keyword is None:
			parts = models.Participant.objects.all()
		else:
			parts=models.Participant.objects.filter(Q(attendee__contains = keyword) | Q(eventId__contains = keyword))
		ser = serializer.ParticipantSerializer(parts , many=True)
		return Response(ser.data , status=status.HTTP_200_OK)
	
	def post(self , request):
		ser = serializer.ParticipantSerializer(data = request.data)
		if ser.is_valid():
			ser.save()
			part = models.Participant.objects.get(pk = ser.data['id'])
			pdfWelcome(part)
			emailTheAttendee(part)
			os.remove(part.pdfFile.path)
			return Response(ser.data , status=status.HTTP_201_CREATED)
		return Response(ser.errors , status=status.HTTP_400_BAD_REQUEST)
	

class ParticipantDetailView(APIView):
	def getParts(self , pk):
		try:
			part = models.Participant.objects.get(pk =pk )
			return part
		except:
			return None
	
	def get(self , request , pk):
		parts = self.getParts(pk)
		if parts is None:
				return Response(status=status.HTTP_404_NOT_FOUND)
		ser = serializer.ParticipantSerializer(parts)
		return Response(ser.data , status=status.HTTP_200_OK)
	
	def put(self , request , pk):
		parts = self.getParts(pk)
		if parts is None:
				return Response(status=status.HTTP_404_NOT_FOUND)
		ser = serializer.ParticipantSerializer(parts , request.data)
		if ser.is_valid():
			ser.save()
			return Response(ser.data,status=status.HTTP_202_ACCEPTED)
		return Response(ser.errors , status.HTTP_400_BAD_REQUEST)
	
	def delete(self , request , pk):
		parts = self.getParts(pk)
		# parts.pdfFile.
		
		if parts is None:
				return Response(status=status.HTTP_404_NOT_FOUND)
		parts.delete()
		return Response(status=status.HTTP_205_RESET_CONTENT)	


#pdf Function

def pdfWelcome(participantId):
	attendeeId = participantId.attendee
	eventId = participantId.eventId
	fileName = f'./welcome{str(participantId)}.pdf'
	participantId.pdfFile= fileName
	participantId.save()
	fileName = participantId.pdfFile.path
	title = eventId.eventName
	documentTitle = 'Congratulation , You have enrolled in the Event'
	subTitle = "Congratulation , You have enrolled in the Event"
	pdf = canvas.Canvas(fileName)
	pdf.setTitle(documentTitle)
	pdf.setFont("Courier-Bold" ,24)
	pdf.drawCentredString(300,770 , title)
	pdf.setFillColorRGB(0, 0, 255) 
	pdf.setFont("Courier-Bold", 18) 
	pdf.drawCentredString(290, 720, subTitle)
	pdf.line(30, 710, 550, 710)
	pdf.drawCentredString(290 , 690 , "Event Detail")
	text = pdf.beginText(40, 660) 
	text.setFont("Courier", 18) 
	text.setFillColor(colors.black) 
	text.textLine(f'Date and Time : {eventId.time.strftime("%B %d, %Y  %H:%M:%S")}')
	text.textLine(f'Venue : {eventId.venue}')
	pdf.drawText(text)
	pdf.line(30 , 630 , 550 , 630)
	pdf.drawCentredString(290 , 600 , "Participants Detail")
	text1 = pdf.beginText(40, 580) 
	text1.setFont("Courier", 18) 
	text1.setFillColor(colors.black) 
	text1.textLine(f'Name : {attendeeId.first_name} {attendeeId.last_name}')
	text1.textLine(f'Age : {attendeeId.age}')
	text1.textLine(f'Unique Code : {str(participantId)}')
	pdf.drawText(text1)
	pdf.save()
	participantId.save()

#Email The User
def emailTheAttendee(participantId):
	eventId = participantId.eventId
	attendee = participantId.attendee
	subject = f'Successfully enrollment in {eventId.eventName}'
	message = f'Hi {attendee.get_full_name()}, thank you for registering in {eventId.eventName}.'
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [attendee.email, ]
	email = EmailMessage(subject , message , email_from , recipient_list)
	try:
		email.attach_file(participantId.pdfFile.path )
		email.send()
	except Exception as e:
         return (e)
	
	