# accounts/models.py
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.db import models
from shortuuid.django_fields import ShortUUIDField
class CustomUser(AbstractUser):
    id = ShortUUIDField(primary_key=True,max_length=20,length=10,prefix="rest",alphabet="abcdefhgigklmnoqz93801 ", unique=True)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)  # Add the otp field here

    # Add custom fields here, if needed

    def __str__(self):
        return self.username
    def profilefun(self):
        profile,created=UserProfile.objects.get_or_create(user=self)
        return profile


 
class House(models.Model):
    id=ShortUUIDField(primary_key=True,max_length=20,length=10,prefix="hom",alphabet="abcdefhgigklm93801")
    image=models.ImageField(upload_to='houses_images')
    salary=models.FloatField(0.0)
    favorit=models.BooleanField(default=False)
    location=models.TextField(default='Beni-Seuf')
    discount=models.FloatField(default=0.0)
    level=models.IntegerField(default=0)
    bedrooms=models.IntegerField(default=0)
    bathrooms=models.IntegerField(default=0)
    area=models.FloatField(default=0.0)
    description=models.CharField(max_length=50,default='null')
    conditions=models.TextField (default='null')
    ava=models.CharField(max_length=100,default='null')
    rev=models.BooleanField(default=False)
    furnished=models.BooleanField(default=False)
    viewer=models.FloatField(default=0.0)
    video=models.FileField(upload_to='vedios_house',default='null')



class categoryModel(models.Model):
    id= ShortUUIDField(primary_key=True,max_length=20,length=10,prefix="cat",alphabet="abcdefhgigklm93801")
    image=models.ImageField(upload_to='categories_images')
    name=models.CharField(max_length=15 )
     
class Banner(models.Model):
    id=ShortUUIDField(primary_key=True,max_length=20,length=10,prefix="bann",alphabet="abcdefhgigklm93801")
    image=models.ImageField(upload_to='banner_images')
 


class UserProfile(models.Model):
    id=ShortUUIDField(primary_key=True,max_length=20,length=10,prefix="pro",alphabet="abcdefhgigklm93801")
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=1000)
    bio = models.CharField(max_length=100)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.full_name == "" or self.full_name == None:
            self.full_name = self.user.username
        super(UserProfile, self).save(*args, **kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
        instance.profilefun().save()
   

post_save.connect(create_user_profile, sender=CustomUser)
post_save.connect(save_user_profile, sender=CustomUser)


 
class ChatMessage(models.Model):
    id= ShortUUIDField(primary_key=True,max_length=20,length=10,prefix="eae",alphabet="abcdefhgigklm93801")
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="user_messages")
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="sent_messages")
    reciever = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="recieved_messages")
    messages = models.TextField (max_length=100000)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['timestamp']
        verbose_name_plural = "Message"
    def str(self):
        return f"{self.sender} - {self.reciever}"   
    @property
    def sender_profile(self):
        sender_profile = UserProfile.objects.get(user=self.sender)
        return sender_profile
    @property
    def reciever_profile(self):
        reciever_profile = UserProfile.objects.get(user=self.reciever)
        return reciever_profile 


class TranslatedText(models.Model):
    text_to_translate = models.TextField()
    target_language = models.TextField()
