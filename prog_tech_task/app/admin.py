from django.contrib import admin
from app.models import *

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name','user_email','user_mobile','user_password','created_at','created_by','updated_at','updated_by','deleted_at','deleted_by')
admin.site.register(UserProfile, UserProfileAdmin)


class UserImagesAdmin(admin.ModelAdmin):
    list_display = ('img_id', 'user','img_name','img_type','image_path','qr_code','created_at','created_by','updated_at','updated_by','deleted_at','deleted_by')
admin.site.register(UserImages, UserImagesAdmin)