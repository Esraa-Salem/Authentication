# accounts/urls.py

from django.urls import path
from .views import UserSerializerlist ,UserINFO,change_password 
from .views import registerapi,user_logout
#from knox import views as views_knox
from .views import *
from .views import LoginWithOTP, ValidateOTP 
from . import views
urlpatterns = [
    path('getall/',UserSerializerlist.as_view(),name='get'),
    path("details/<str:id>/",UserINFO.as_view()),
    path('register/',registerapi.as_view(),name='register'),
    path('login/',loginapi.as_view(),name='login'),
    path('logout/',user_logout,name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('login-with-otp/', LoginWithOTP.as_view(), name='login-with-otp'),
    path('validate-otp/', ValidateOTP.as_view(), name='validate-otp'),
    #House
    path('allHouses/',HouseSerializerlist.as_view()),
    path("detailsHouse/<str:id>/",HouseINFO.as_view()),
    #category
    path('allCategories/',CategorySerializerlist.as_view()),
    path("detailsCategory/<str:id>/",CategoryINFO.as_view()),
    #Banner
    path('allBanners/',BannerSerializerlist.as_view()),
    #Chat/Text Messaging 
    path("my-messages/<str:user_id>/", views.MyInbox.as_view()),
    path("get-messages/<sender_id>/<reciever_id>/", views.GetMessages.as_view()),
    path("send-messages/", views.SendMessages.as_view()),
    
    # Get profile
    path("profile/<str:pk>/", views.ProfileDetail.as_view()),
    path("search/<username>/", views.SearchUser.as_view()),
    path('listprofile/',ProfileSerializerlist.as_view()), 
    path('translate/',TranslationAPIView.as_view()),




    #offer & request
    ############################## new task ########################
    path('offer',views.offerList.as_view(),name='user'),
    path('offer/new', views.new_offer,name='new_offer'),
    path('offer/<int:id>/',views.offerDetails.as_view()),
    path('addoffer',views.Addofferr.as_view()),
    path('addoffer/<int:id>/',views.Addoffer.as_view()),
    path('request',views.Requestlist.as_view()),
    path('request/new', views.new_Request,name='new_request'),
    path('request/<int:id>/',views.RequestDetails.as_view()),
    path('comment',views.commentlist.as_view()),
    path('comment/new', views.new_comment,name='new_comment'),
    path('comment/<int:id>/',views.commentDetails.as_view()),
] 
 