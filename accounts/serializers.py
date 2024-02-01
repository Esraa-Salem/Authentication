from rest_framework import serializers
from django.contrib.auth.models import User,AbstractUser
from .models import  *
# class UserSerializer(serializers.ModelSerializer):
#     password=serializers.CharField(max_length=65,min_length=8,write_only=True)
#     email=serializers.EmailField(max_length=255,min_length=4 )
#     first_name=serializers.CharField(max_length=65,min_length=2)
#     last_name=serializers.CharField(max_length=65,min_length=2)
    
#     class Meta:
#         model=User
#         fields= ['id','username','first_name','last_name','email','password'  ]

#     def validate(self,attrs):
#         if User.objects.filter(email=attrs['email']).exists():
#             raise serializers.ValidationError({'email',('Email is already in use')})  
#         return super().validate(attrs)
# #to make authentication password and username
#     def create (self,validated_data):
#         return User.objects.create_user(validated_data)

 
class UserSerializer(serializers.ModelSerializer):   
    class Meta:
        username=serializers.CharField(max_length=65,min_length=6)
       # is_email_confirmed=serializers.BooleanField(default=False)
        model=CustomUser
        fields=('id','username','email','otp') 
class RegisterSerializer(serializers.ModelSerializer):
            class Meta:
              model=CustomUser
              fields=('id','username','email','password')
              extra_kwargs={'password':{'write_only':True}} 
            def create (self,validated_data):
               user=  CustomUser.objects.create_user(validated_data['username'],validated_data['email'],validated_data['password']) 
               return user 

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)    

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model=House
        fields='__all__'


class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model=categoryModel
        fields='__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banner
        fields='__all__'

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields ='__all__'
    
    def init(self, *args, **kwargs):
        super(ProfileSerializer, self).init(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class MessageSerializer(serializers.ModelSerializer):
    reciever_profile = ProfileSerializer(read_only=True)
    sender_profile = ProfileSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = '__all__'
    def init(self, *args, **kwargs):
        super(MessageSerializer, self).init(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method=='POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2




 
        




 
        




 
        

