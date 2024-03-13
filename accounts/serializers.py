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
    image_url =  serializers.SerializerMethodField()

    class Meta:
        model=Banner
        fields=('id','image','image_url')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None

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


class translateserializer(serializers.ModelSerializer):
        class Meta:
          model= TranslatedText
          fields='__all__'



 
######################## new task ##########################
          
class offerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=offerImages
        fields=['id','offerimg','images']




class offerSerializer(serializers.ModelSerializer):
    user_username =serializers.ReadOnlyField(source='user.username')
    img= offerImageSerializer(many=True,read_only=True)
    uploaded_images=serializers.ListField(
        child=serializers.ImageField(max_length=1000000 ,allow_empty_file=False ,use_url=False),
        write_only=True
    )
    class Meta:
        model= OfferModels
        fields = ['id','user_username','phone_number','rent_start_time','rent_finish_time','price','location','level','bedrooms','bathrooms','area','description','conditions','ava','rev','furnished','img','uploaded_images']
        
    def create(self,validated_data):
        uploaded_images =validated_data.pop("uploaded_images")
        offerimg=OfferModels.objects.create(**validated_data)
        for images in uploaded_images:
            offer_image=offerImages.objects.create(offerimg=offerimg,images=images)
            
        return offerimg
        

          


class addofferSerializer(serializers.ModelSerializer):
    class Meta:
        model=AddOffer
        fields='__all__'
        


class requesrSerializer(serializers.ModelSerializer):
    user_username =serializers.ReadOnlyField(source='user.username')
    class Meta:
        model=Request
        fields=['id','user_username','images' , 'date','text' ]



class commentSerializer(serializers.ModelSerializer):
    user_username =serializers.ReadOnlyField(source='user.username')
    profile_image = serializers.SerializerMethodField()
    requests= requesrSerializer(many=True, read_only=True)
    class Meta:
        model=CommentModels
        fields= ['id','user_username','profile_image' , 'date','text' , 'requests']

    
    def get_profile_image(self, obj):
        user_profile = UserProfile.objects.get(user=obj.user)
        if user_profile.image:
            return user_profile.image.url
        return None





 
        




 
        

