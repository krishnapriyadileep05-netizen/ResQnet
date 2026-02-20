from django.db import models
from Guest.models import *

# # Create your models here.
class tbl_complaint(models.Model):
    complaint_title=models.CharField(max_length=50)
    complaint_description=models.CharField(max_length=100)
    user_id=models.ForeignKey(tbl_user,on_delete=models.CASCADE,null=True)
    volunteer_id=models.ForeignKey(tbl_volunteer,on_delete=models.CASCADE,null=True)
    complaint_status=models.IntegerField(default=0)
    complaint_date=models.DateField(auto_now_add=True)
    complaint_reply=models.CharField(max_length=50,null=True)

class tbl_request(models.Model):
    request_title = models.CharField(max_length=50)
    request_content = models.CharField(max_length=100)
    request_date = models.DateField(auto_now_add=True)
    request_todate = models.DateField()
    request_status = models.IntegerField(default=0)
    request_type = models.IntegerField(default=0)  
    place_id = models.ForeignKey(tbl_place, on_delete=models.CASCADE)
    user_id = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    request_message = models.CharField(max_length=255, blank=True, null=True)


class tbl_feedback(models.Model):
    feedback_date=models.DateField(auto_now_add=True)
    feedback_content=models.CharField(max_length=100)
    user_id=models.ForeignKey(tbl_user,on_delete=models.CASCADE)

class tbl_payment(models.Model):
    payment_amount=models.CharField(max_length=50)
    payment_date=models.DateField(auto_now_add=True)
    user_id=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
  


    
