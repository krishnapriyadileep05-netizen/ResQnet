from django.db import models


# Create your models here.
class tbl_district(models.Model):
    district_name=models.CharField(max_length=50)
class tbl_admin(models.Model):
    admin_name=models.CharField(max_length=50)
    admin_email=models.CharField(max_length=50)
    admin_password=models.CharField(max_length=50)
class tbl_category(models.Model):
    category_name=models.CharField(max_length=50)

class tbl_place(models.Model):
    place_name = models.CharField(max_length=50)
    district = models.ForeignKey(tbl_district,on_delete=models.CASCADE)

class tbl_subcategory(models.Model):
    subcategory_name=models.CharField(max_length=50)
    category=models.ForeignKey(tbl_category,on_delete=models.CASCADE)

class tbl_awareness(models.Model):
    awareness_title=models.CharField(max_length=200)
    awareness_description=models.TextField()
    awareness_image=models.FileField(upload_to='Awareness/')
    awareness_date=models.DateField(auto_now_add=True)
    awareness_status=models.IntegerField(default=0)  # 0=Active, 1=Inactive


