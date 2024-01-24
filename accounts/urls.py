# accounts/urls.py

from django.urls import path
from .views import UserSerializerlist ,UserINFO,change_password 
from .views import registerapi,user_logout
#from knox import views as views_knox
from .views import loginapi
from .views import LoginWithOTP, ValidateOTP 

urlpatterns = [
    path('getall/',UserSerializerlist.as_view(),name='get'),
    path("details/<str:id>/",UserINFO.as_view()),
    path('register/',registerapi.as_view(),name='register'),
    path('login/',loginapi.as_view(),name='login'),
    path('logout/',user_logout,name='logout'),
    # path("info",userinformationAPIVIEW.as_view()),
    # path("sendconfirmationemail",Sendemailconfirmation.as_view()),
   
    path('change_password/', change_password, name='change_password'),
    
    path('login-with-otp/', LoginWithOTP.as_view(), name='login-with-otp'),
    path('validate-otp/', ValidateOTP.as_view(), name='validate-otp'),

    #path('logoutall/',views_knox.LogoutAllView.as_view(),name='logoutall')
] 
 