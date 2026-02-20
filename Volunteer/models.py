from django.db import models
from Guest.models import *
from User.models import *

# Create your models here.
class tbl_response(models.Model):
    response_date=models.DateField(auto_now_add=True)
    response_status=models.IntegerField(default=0)
    volunteer_id=models.ForeignKey(tbl_volunteer,on_delete=models.CASCADE)
    request_id=models.ForeignKey(tbl_request,on_delete=models.CASCADE)

class tbl_camp(models.Model):
    camp_details=models.CharField(max_length=100)
    camp_date=models.DateField(auto_now_add=True)
    camp_status=models.IntegerField(default=0)
    place_id=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    volunteer_id=models.ForeignKey(tbl_volunteer,on_delete=models.CASCADE)

class tbl_donationrequest(models.Model):
    donationrequest_date=models.DateField(auto_now_add=True)
    donationrequest_status=models.IntegerField(default=0)
    donationrequest_details=models.CharField(max_length=100)
    place_id=models.ForeignKey(tbl_place,on_delete=models.CASCADE)
    user_id=models.ForeignKey(tbl_user,on_delete=models.CASCADE,null=True)

class tbl_donationitems(models.Model):
    donationitems_name=models.CharField(max_length=100)
    donationitems_count=models.CharField(max_length=100)
    donationrequest_id=models.ForeignKey(tbl_donationrequest,on_delete=models.CASCADE,null=True)
    

class tbl_donation(models.Model):
    donation_date=models.DateField(auto_now_add=True)
    donation_status=models.IntegerField(default=0)
    donation_type=models.CharField(max_length=100)
    donation_remark=models.CharField(max_length=100)
    donation_amount=models.CharField(max_length=100)
    donationitem_id=models.ForeignKey(tbl_donationitems,on_delete=models.CASCADE,null=True)
    user_id=models.ForeignKey(tbl_user,on_delete=models.CASCADE,null=True)
    volunteer_id=models.ForeignKey(tbl_volunteer,on_delete=models.CASCADE,null=True)

class tbl_assigndonation(models.Model):
    assigndonation_date=models.DateField(auto_now_add=True)
    assigndonation_status=models.IntegerField(default=0)
    assigndonation_description=models.CharField(max_length=100)
    volunteer_id=models.ForeignKey(tbl_volunteer,on_delete=models.CASCADE)
    place_id=models.ForeignKey(tbl_place,on_delete=models.CASCADE)


class tbl_collectionrequest(models.Model):
    request_date = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=0)

    donation_id = models.ForeignKey(tbl_donation, on_delete=models.CASCADE)
    delivery_place = models.ForeignKey(tbl_place, on_delete=models.CASCADE,null=True)
    volunteer_id = models.ForeignKey(tbl_volunteer, on_delete=models.CASCADE, null=True)

class tbl_team(models.Model):
    team_name=models.CharField(max_length=100)
    team_photo=models.FileField(upload_to="Assets/VolunteerDocs/")
    team_address=models.CharField(max_length=100)
    team_gender=models.CharField(max_length=100)
    team_dob=models.DateField()
    team_contact=models.CharField(max_length=100)
    volunteer_id=models.ForeignKey(tbl_volunteer,on_delete=models.CASCADE)

class tbl_taskmember(models.Model):
    response_id = models.ForeignKey(tbl_response, on_delete=models.CASCADE)
    collectionrequest = models.ForeignKey(tbl_collectionrequest,on_delete=models.CASCADE,null=True)
    team_id = models.ForeignKey(tbl_team, on_delete=models.CASCADE,null=True)
