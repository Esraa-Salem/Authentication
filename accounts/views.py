# accounts/views.py


from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from .serializers import *
#from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from rest_framework import viewsets,generics,permissions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token 
# Create your views here.
from knox.models import AuthToken
from knox.views import LoginView as knoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import authentication_classes,permission_classes,api_view
from rest_framework.permissions import IsAuthenticated
# from .models import EmalconfirmationToken
# from .utils import send_confirmation_email

from .serializers import ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('old_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'success':'True','message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'success':'False','error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class registerapi(generics.GenericAPIView):
    serializer_class=RegisterSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user= serializer.save()
        return Response({'success':'True',
            'status':200,'msg':'created success',
            'data':serializer.data,
            #'token':AuthToken.objects.create(user)[1]
             
        })

class loginapi(knoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post (self,request,format=None):
         
         serializer=AuthTokenSerializer(data=request.data)
         #serializer.is_valid(raise_exception=False)
        
         if serializer.is_valid():
            user=serializer.validated_data['user']
            login(request,user)
            super(loginapi,self).post(request,format=None)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'success':'True',
                'status':200,'msg':'login success',
                'data':request.data,
                'token':  token.key
                
             })
         else:         
                 return Response({'success':'False','status':400,'error':'There is wrong in Username or password, Please review your data and try again'})
                
         

 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.delete()
            return Response({'success':'True','status':200,'data':'null','message': 'Successfully logged out.'})
        except Exception as e:
            return Response({'success':'False','status':400,'error': str(e)})

 
class UserSerializerlist(APIView ):
  
     def get(self,request):
         users=CustomUser.objects.all()
         data=UserSerializer(users,many=True).data
         return Response(data)
    

class UserINFO(APIView): 
     
     def get(self,request,id):
         try:
             users=CustomUser.objects.get(id=id)
         except CustomUser.DoesNotExist:
             return Response({'success':'False','status':404,'errors':serializer.errors,'msg':'not found'} )
         serializer=UserSerializer(users)
        
         return Response({'success':'True','status':200,'data':serializer.data,'msg':'created success'})
       
 
     def put(self,request,id):
           try:
             users=CustomUser.objects.get(id=id)
           except CustomUser.DoesNotExist:
             return Response({'success':'False','status':404,'errors':serializer.errors,'msg':'id not found'} )
           serializer=UserSerializer(users,data=request.data)
          
           if serializer.is_valid():
                 serializer.save()
             
                 return Response({'success':'True','status':200,'data':serializer.data,'msg':'Updated successfully'} )
          
        
           return Response({'success':'False','status':404,'errors':serializer.errors,'msg':'Updated failed'} )
          
     def delete(self,request,id):
          try:
             user=CustomUser.objects.get(id=id)
          except CustomUser.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
         
          user.delete()
          return Response({'status':200,'msg':'deleted is done'} )





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_otp, send_otp_email
from .models import *

class LoginWithOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'success':'False','error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        user.otp = otp
        user.save()

        send_otp_email(email, otp)
        # send_otp_phone(phone_number, otp)

        return Response({'success':'True','message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)


# accounts/views.py

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class ValidateOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'success':'False','error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.otp = None  # Reset the OTP field after successful validation
            user.save()

            # Authenticate the user and create or get an authentication token
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'success':'True','token': token.key} , status=status.HTTP_200_OK)
        else:
            return Response({'success':'False','error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        


from django.db.models import Q,OuterRef,Subquery
class MyInbox(generics.ListAPIView): 
    serializer_class = MessageSerializer 

    def get_queryset(self): 
        user_id = self.kwargs['user_id'] 

        last_msg = Subquery(
            ChatMessage.objects.filter( 
                Q(sender=OuterRef('id'), reciever=user_id) | 
                Q(reciever=OuterRef('id'), sender=user_id) 
            ).order_by('-timestamp')[:1].values('timestamp')
        )

        messages = ChatMessage.objects.filter( 
            id__in=Subquery( 
                CustomUser.objects.filter( 
                    Q(sent_messages__reciever=user_id) | Q(recieved_messages__sender=user_id) 
                ).distinct().annotate( 
                    last_msg=last_msg
                ).values_list('last_msg').order_by("-last_msg") 
            ) 
        ).order_by("-timestamp")
    
        return messages
  
    
class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        sender_id = self.kwargs['sender_id']
        reciever_id = self.kwargs['reciever_id']
        messages =  ChatMessage.objects.filter(sender_id__in=[sender_id, reciever_id], reciever_id__in=[sender_id, reciever_id])
        return messages

# from django.utils.decorators import method_decorator    
# from django.contrib.auth.decorators import login_required
# @method_decorator(login_required, name='dispatch')
class SendMessages(generics.CreateAPIView):
    serializer_class = MessageSerializer

 
class ProfileSerializerlist(APIView):
    def get(self, request):
        housess = UserProfile.objects.all()
        serializer = ProfileSerializer(housess, many=True)
        return Response({
            'status':200,'msg':'success',
            'data':serializer.data
             
        })
class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = UserProfile.objects.all()
    #permission_classes = [IsAuthenticated]  


class SearchUser(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]  

    def list(self, request, *args, **kwargs):
        username = self.kwargs['username']
        logged_in_user = self.request.user
        users = UserProfile.objects.filter(Q(user__username__icontains=username) | Q(full_name__icontains=username) | Q(user__email__icontains=username) & 
                                       ~Q(user=logged_in_user))

        if not users.exists():
            return Response(
                {"detail": "No users found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
#Banner...
class BannerSerializerlist(APIView):
    def get(self, request):
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response({
            'status':200,'msg':'success',
            'data':serializer.data
             
        })

    def post(self, request):
        serializer = BannerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
            'status':200,'msg':'created success',
            'data':serializer.data
             
        })
        return Response({
            'status':400,'msg':'failed created',
            'data':serializer.data,
            'errors':serializer.errors
             
        })



# #House....
class HouseSerializerlist(APIView):
    def get(self, request):
        housess = House.objects.all()
        serializer = HouseSerializer(housess, many=True)
        return Response({
            'status':200,'msg':'success',
            'data':serializer.data
             
        })

    def post(self, request):
        serializer = HouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
            'status':200,'msg':'created success',
            'data':serializer.data
             
        })
        return Response({
            'status':400,'msg':'failed created',
            'data':serializer.data,
            'errors':serializer.errors
             
        })
    
  

class HouseINFO(APIView): 
     
     def get(self,request,id):
         try:
             houses=House.objects.get(id=id)
         except House.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'not found'} )
         serializer=HouseSerializer(houses)
        
         return Response({'status':200,'data':serializer.data,'msg':'created success'})

  
 
     def put(self,request,id):
           try:
             houses=House.objects.get(id=id)
           except House.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
           serializer= HouseSerializer(houses,data=request.data)
          
           if serializer.is_valid():
                 serializer.save()
             
                 return Response({'status':200,'msg':'Updated successfully'} )
          
        
           return Response({'status':404,'errors':serializer.errors,'msg':'Updated failed'} )
          
     def delete(self,request,id):
          try:
             house=House.objects.get(id=id)
          except House.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
        
          house.delete()
          return Response({'status':200,'msg':'deleted is done'} )


#categories...
class CategorySerializerlist(APIView):
    def get(self, request):
        categories = categoryModel.objects.all()
        serializer = categorySerializer(categories, many=True)
        return Response({
            'status':200,'msg':'success',
            'data':serializer.data
             
        })

    def post(self, request):
        serializer = categorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
            'status':200,'msg':'created success',
            'data':serializer.data
             
        })
        return Response({
            'status':400,'msg':'failed created',
            'data':serializer.data,
            'errors':serializer.errors
             
        })
     


class CategoryINFO(APIView): 
     
     def get(self,request,id):
         try:
             categories=categoryModel.objects.get(id=id)
         except categoryModel.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'not found'} )
         serializer=categorySerializer(categories)
        
         return Response({'status':200,'data':serializer.data,'msg':'created success'})
     


     def put(self,request,id):
           try:
             categories=categoryModel.objects.get(id=id)
           except categoryModel.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
           serializer=categorySerializer(categories,data=request.data)
          
           if serializer.is_valid():
                 serializer.save()
             
                 return Response({'status':200,'msg':'Updated successfully'} )
          
        
           return Response({'status':404,'errors':serializer.errors,'msg':'Updated failed'} )
          
     def delete(self,request,id):
          try:
             category=categoryModel.objects.get(id=id)
          except categoryModel.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
        
          category.delete()
          return Response({'status':200,'msg':'deleted is done'} )
             

#translation
from googletrans import Translator
class TranslationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        text_to_translate = request.data.get('text_to_translate', '')
        target_language = request.data.get('target_language', 'ar')

        translator = Translator()
        translated_text = translator.translate(text_to_translate, dest=target_language).text

        # التحقق من أن النص المترجم ليس None قبل تحويله إلى JSON
        if translated_text is not None:
            return Response({'translated_text': translated_text})
        else:
            return Response({'error': 'Translation failed'})

 
 
        