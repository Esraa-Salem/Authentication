from django.contrib import admin

# Register your models here.
from .models import  *
 
class ChatMessageAdmin(admin.ModelAdmin):
    list_editable=['is_read']
    list_display=['sender','reciever','messages','is_read']
admin.site.register(CustomUser)    
admin.site.register(ChatMessage,ChatMessageAdmin)
admin.site.register(OfferModels) 