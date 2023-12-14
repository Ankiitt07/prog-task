from django.db import models

# Create your models here.

# For User Table in database.
class UserProfile(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=200, blank=True)
    user_email = models.CharField(max_length=100, blank=True)
    user_mobile = models.CharField(max_length=100, blank=True)
    user_password = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default="0")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default="0")
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.IntegerField(default="0")

    def __str__(self):
        return self.user_name

    class Meta:
        db_table = 'user_table'
        managed = True


class UserImages(models.Model):
    img_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    img_name = models.CharField(max_length=200, blank=True)
    img_type = models.CharField(max_length=100, blank=True)
    image_path = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank= True)
    qr_code = models.ImageField(upload_to='qr_code/', blank= True)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(default="0")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.IntegerField(default="0")
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.IntegerField(default="0")

    def __str__(self):
        return self.img_name

    class Meta:
        db_table = 'user_img_table'
        managed = True