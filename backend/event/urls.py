from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
	path('' , view=views.home , name='home'),
	#For User
	path('user' , views.UserListView.as_view() , name='userlist'),
	path('user/<str:id>/<str:password>' , views.UserDetailView.as_view()),
	path('user/<str:id>' , views.UserDetailView.as_view()),
	path('logout' , views.logoutUser),
	path('inactiveUser' , views.GetInActiveUser.as_view()),
	path('activeUser/<ids>' , views.MakeActiveUser.as_view()),

	#Event
	path('event' , views.EventListView.as_view()),
	path('event/<str:attribute>/<str:keyword>' , views.EventListView.as_view()),#for filter
	path('event/<str:pk>' , view=views.EventDetailView.as_view()),

	#For Participant
	path('parts' , views.ParticipantsListView.as_view()),
	path('parts/<str:keyword>' , views.ParticipantsListView.as_view()),#For filter,
	path('part/<int:pk>' , views.ParticipantDetailView.as_view())
	
]