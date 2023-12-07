# accounts/views.py


from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer,RegisterSerializer 
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
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class registerapi(generics.GenericAPIView):
    serializer_class=RegisterSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user= serializer.save()
        return Response({
            'status':200,'msg':'created success',
            'token':AuthToken.objects.create(user)[1]
             
        })

class loginapi(knoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post (self,request,format=None):
         serializer=AuthTokenSerializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         user=serializer.validated_data['user']
         login(request,user)
         return super(loginapi,self).post(request,format=None)


 
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
            return Response({'status':200,'message': 'Successfully logged out.'})
        except Exception as e:
            return Response({'status':400,'error': str(e)})

 
class UserSerializerlist(APIView):
     
     def get(self,request):
         users=CustomUser.objects.all()
         data=UserSerializer(users,many=True).data
         return Response(data)
    

class UserINFO(APIView): 
     
     def get(self,request,id):
         try:
             users=CustomUser.objects.get(id=id)
         except CustomUser.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'not found'} )
         serializer=UserSerializer(users)
        
         return Response({'status':200,'data':serializer.data,'msg':'created success'})
       
 
     def put(self,request,id):
           try:
             users=CustomUser.objects.get(id=id)
           except CustomUser.DoesNotExist:
             return Response({'status':404,'errors':serializer.errors,'msg':'id not found'} )
           serializer=UserSerializer(users,data=request.data)
          
           if serializer.is_valid():
                 serializer.save()
             
                 return Response({'status':200,'msg':'Updated successfully'} )
          
        
           return Response({'status':404,'errors':serializer.errors,'msg':'Updated failed'} )
          
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
from .models import CustomUser

class LoginWithOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        user.otp = otp
        user.save()

        send_otp_email(email, otp)
        # send_otp_phone(phone_number, otp)

        return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)


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
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.otp = None  # Reset the OTP field after successful validation
            user.save()

            # Authenticate the user and create or get an authentication token
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)