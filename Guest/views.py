from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
# Create your views here.
def indexpage(request):
    return render(request,'Guest/Indexpage.html')
def UserRegistration(request):
    district = tbl_district.objects.all()
    place = tbl_place.objects.all()

    if request.method == "POST":
        name = request.POST.get("txt_name")
        email = request.POST.get("txt_email")
        contact = request.POST.get("txt_contact")
        address = request.POST.get("txt_address")
        password = request.POST.get("txt_password")
        confirm = request.POST.get("txt_password")  

        photo = request.FILES.get("file_photo")
        place = tbl_place.objects.get(id=request.POST.get("sel_place"))

        if password != confirm:  
            return render(
                request,
                'Guest/UserRegistration.html',
                {
                    'msg': "Password and Confirm Password do not match",
                    'district': district,
                    'place': place
                }
            )

        checkuseremail = tbl_user.objects.filter(user_email=email).count()
        if checkuseremail > 0:
            return render(
                request,
                'Guest/UserRegistration.html',
                {
                    'msg': "Email Already Exist",
                    'district': district,
                    'place': place
                }
            )
        else:
            tbl_user.objects.create(
                user_name=name,
                user_email=email,
                user_contact=contact,
                user_address=address,
                user_password=password,
                user_photo=photo,
                place=place
            )
            return render(request, 'Guest/UserRegistration.html', {'msg': 'Registered'})

    else:
        return render(request, 'Guest/UserRegistration.html', {'district': district, 'place': place})

def AjaxPlace(request):
    district=tbl_district.objects.get(id=request.GET.get("did"))
    place=tbl_place.objects.filter(district=district)
    return render(request,'Guest/AjaxPlace.html',{"place":place})

def Login(request):
    
    if request.method == "POST":
        email=request.POST.get("txt_email")
        password=request.POST.get("txt_password")
    

        admincount=tbl_admin.objects.filter(admin_email=email,admin_password=password).count()
        usercount=tbl_user.objects.filter(user_email=email,user_password=password).count()
        volunteercount=tbl_volunteer.objects.filter(volunteer_email=email,volunteer_password=password).count()


        if admincount>0:
            admindata=tbl_admin.objects.get(admin_email=email,admin_password=password)
            request.session["aid"]=admindata.id
            return redirect("Admin:HomePage")
        elif usercount>0:
            userdata=tbl_user.objects.get(user_email=email,user_password=password)
            request.session["uid"]=userdata.id
            return redirect("User:HomePage")
        elif volunteercount>0:
            volunteerdata=tbl_volunteer.objects.get(volunteer_email=email,volunteer_password=password)
            if volunteerdata.volunteer_status == 1:
                request.session["vid"]=volunteerdata.id
                return redirect("Volunteer:HomePage")
            elif volunteerdata.volunteer_status == 2:
                return render(request,'Guest/Login.html',{'msg':' Your Account is Blocked My Admin. '})
            else :
                return render(request,'Guest/Login.html',{'msg':' Your Account Verification is Pending... '})
        else:
            return render(request,'Guest/Login.html',{'msg':' Invalid Email or Password '})
    else:
        return render(request,'Guest/Login.html')
            
def Volunteer(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")
    
    district = tbl_district.objects.all()
    place = tbl_place.objects.all()

    if request.method == "POST":
        name = request.POST.get("txt_name")
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        confirm = request.POST.get("txt_confirm") 
        photo = request.FILES.get("file_photo")
        proof = request.FILES.get("file_proof")
        address = request.POST.get("txt_address")
        contact = request.POST.get("txt_contact")
        emergency = 1 if request.POST.get("txt_emergency") == "1" else 0

        place_obj = tbl_place.objects.get(id=request.POST.get("sel_place"))
        checkemail = tbl_volunteer.objects.filter(volunteer_email=email).count()

        if checkemail > 0:
            return render(request, "Guest/Volunteer.html", {'msg': "Email Already Exist"})
        elif password != confirm:
            return render(request, "Guest/Volunteer.html", {'msg': "Password and Confirm Password do not match"})
        else:
            tbl_volunteer.objects.create(
                volunteer_name=name,
                volunteer_email=email,
                volunteer_password=password,
                volunteer_photo=photo,
                volunteer_proof=proof,
                volunteer_address=address,
                volunteer_contact=contact,
                place=place_obj,
                volunteer_emergency=emergency
            )
            return render(request, 'Guest/Volunteer.html', {'msg': 'Data inserted successfully'})
    else:
        return render(request, 'Guest/Volunteer.html', {'districts': district, 'place': place})