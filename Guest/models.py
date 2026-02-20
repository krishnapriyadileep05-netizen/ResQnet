from django.db import models
from Admin.models import *
class tbl_user(models.Model):
    user_name=models.CharField(max_length=50)
    user_email=models.CharField(max_length=50)
    user_contact=models.CharField(max_length=50)
    user_address=models.CharField(max_length=100)
    user_password=models.CharField(max_length=50)
    user_photo=models.FileField(upload_to="Assets/UserDocs/")
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    user_status=models.IntegerField(default=0)
  
class tbl_volunteer(models.Model):
    
    volunteer_name=models.CharField(max_length=50)
    volunteer_email=models.CharField(max_length=50)
    volunteer_password=models.CharField(max_length=50)
    volunteer_photo=models.FileField(upload_to="Assets/VolunteerDocs/")
    volunteer_proof=models.FileField(upload_to="Assets/VolunteerDocs/")
    volunteer_address=models.CharField(max_length=100)
    volunteer_contact=models.CharField(max_length=50)
    volunteer_emergency=models.IntegerField()
    place=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    volunteer_status=models.IntegerField(default=0)

