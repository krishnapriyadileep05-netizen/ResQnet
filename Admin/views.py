from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from User.models import *
from Volunteer.models import *
from datetime import date, timedelta
from django.db.models import Sum
from django.db.models import Count
# Create your views here.
def logout(request):
    del request.session["aid"]
    return redirect("Guest:Login")

def AdminRegistration(request):
    data = tbl_admin.objects.all()

    if request.method == "POST":
        name = request.POST.get("txt_name")
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        confirm = request.POST.get("txt_confirm")  

        if password != confirm:  
            return render(
                request,
                'Admin/AdminRegistration.html',
                {'msg': "Password and Confirm Password do not match"}
            )

        checkemail = tbl_admin.objects.filter(admin_email=email).count()
        if checkemail > 0:
            return render(
                request,
                'Admin/AdminRegistration.html',
                {'msg': "Email Already Exist"}
            )
        else:
            tbl_admin.objects.create(
                admin_name=name,
                admin_email=email,
                admin_password=password
            )
            return render(
                request,
                'Admin/AdminRegistration.html',
                {'msg': 'Data inserted'}
            )
    else:
        return render(request, 'Admin/AdminRegistration.html', {"AdminRegistration": data})

def HomePage(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        return render(request,"Admin/HomePage.html")

def District(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:

        data=tbl_district.objects.all()
        if request.method=="POST":
            district=request.POST.get("txt_name")
            checkdistrict = tbl_district.objects.filter(district_name=district).count()
            if checkdistrict > 0:
                return render(request,'Admin/District.html',{'msg':"District Already Exist"})
            else:
                tbl_district.objects.create(district_name=district)

            return render(request,'Admin/District.html',{'msg':'data inserted'})
            
        else:
            return render(request,'Admin/District.html',{"district":data})
    
def Category(request):
    data=tbl_category.objects.all()

    if request.method=="POST":
        category=request.POST.get("txt_category")
        tbl_category.objects.create(category_name=category)

        return render(request,'Admin/Category.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/Category.html',{"category":data})

def deldistrict(request,id):
    tbl_district.objects.get(id=id).delete()
    return redirect("Admin:District")
def editdistrict(request,id):
    editdata=tbl_district.objects.get(id=id)
    if request.method=="POST":
        district=request.POST.get("txt_name")
        editdata.district_name=district
        editdata.save()
        return redirect("Admin:District")
    else:
        return render(request,'Admin/District.html',{'editdata':editdata})

def delcategory(request,id):
    tbl_category.objects.get(id=id).delete()
    return redirect("Admin:Category")
def editcategory(request,id):
    editdata=tbl_category.objects.get(id=id)
    if request.method=="POST":
        category=request.POST.get("txt_category")
        editdata.category_name=category
        editdata.save()
        return redirect("Admin:Category")
    else:
        return render(request,'Admin/Category.html',{'editdata':editdata})

        
def delAdminRegistration(request,id):
    tbl_admin.objects.get(id=id).delete()
    return redirect("Admin:AdminRegistration")
def editAdminRegistration(request,id):
    editdata=tbl_admin.objects.get(id=id)
    if request.method=="POST":
        AdminRegistration=request.POST.get("txt_name")
        editdata.admin_name=AdminRegistration
        
        editdata.save()
        return redirect("Admin:AdminRegistration")
    else:
        return render(request,'Admin/AdminRegistration.html',{'editdata':editdata})

def Place(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        data=tbl_district.objects.all()
        placedata=tbl_place.objects.all()
        if request.method=="POST":
            place=request.POST.get("txt_name")
            district = tbl_district.objects.get(id=request.POST.get("sel_district"))
            tbl_place.objects.create(place_name=place, district=district)

            return render(request,'Admin/Place.html',{'msg':'data inserted'})
        else:
            return render(request,'Admin/Place.html',{"district":data,'place':placedata})

        
def delplace(request,id):
    tbl_place.objects.get(id=id).delete()
    return redirect("Admin:Place")
def editplace(request,id):
    district=tbl_district.objects.all()
    editdata=tbl_place.objects.get(id=id)
    if request.method=="POST":
        Place=request.POST.get("txt_name")
        editdata.district=tbl_district.objects.get(id=request.POST.get("sel_district"))
        editdata.place_name=Place
        editdata.save()
        return redirect("Admin:Place")
    else:
        return render(request,'Admin/Place.html',{'editdata':editdata,'district':district})

def Subcategory(request):
    cdata=tbl_category.objects.all()
    sdata=tbl_subcategory.objects.all()
    if request.method=="POST":
        subcategory=request.POST.get("txt_subcategory")
        category=tbl_category.objects.get(id=request.POST.get("sel_category"))
        tbl_subcategory.objects.create(subcategory_name=subcategory, category=category)


        return render(request,'Admin/Subcategory.html',{'msg':'data inserted'})
    else:
        return render(request,'Admin/Subcategory.html',{"category":cdata,'subcategory':sdata})

def delsub(request,id):
    tbl_subcategory.objects.get(id=id).delete()
    return redirect("Admin:Subcategory")

def editsub(request,id):
    category=tbl_category.objects.all()
    editdata=tbl_subcategory.objects.get(id=id)
    if request.method=="POST":
        Subcategory=request.POST.get("txt_subcategory")
        editdata.category=tbl_category.objects.get(id=request.POST.get("sel_category"))
        editdata.subcategory_name=Subcategory
        
        editdata.save()
        return redirect("Admin:Subcategory")
    else:
        return render(request,'Admin/Subcategory.html',{'editdata':editdata,'category':category})

def UserList(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        userdata=tbl_user.objects.all()
        return render(request,'Admin/UserList.html',{"users":userdata,})
    
def blockuser(request,id):
    udata=tbl_user.objects.get(id=id)
    udata.user_status=1
    udata.save()
    return redirect("Admin:UserList")


def VolunteerList(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        pending=tbl_volunteer.objects.filter(volunteer_status = 0)
        accept=tbl_volunteer.objects.filter(volunteer_status = 1)
        reject=tbl_volunteer.objects.filter(volunteer_status = 2)
        return render(request,'Admin/VolunteerList.html',{"pending":pending,'accept':accept,'reject':reject})
    
def acceptvolunteer(request,id):
    vdata=tbl_volunteer.objects.get(id=id)
    vdata.volunteer_status=1
    vdata.save()
    return redirect("Admin:VolunteerList")

def rejectvolunteer(request,id):
    vdata=tbl_volunteer.objects.get(id=id)
    vdata.volunteer_status=2
    vdata.save()
    return redirect("Admin:VolunteerList")

def viewrequest(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")

    today = date.today()
    upcoming_days = today + timedelta(days=3)

    pending_raw = tbl_request.objects.filter(request_status=0)
    accept_raw = tbl_request.objects.filter(request_status=1)
    reject_raw = tbl_request.objects.filter(request_status=2)

    pending = []
    for r in pending_raw:
        if r.request_todate >= today:
            r.is_important = today <= r.request_todate <= upcoming_days
            pending.append(r)

    accept = []
    for r in accept_raw:
        if r.request_todate >= today:
            r.is_important = today <= r.request_todate <= upcoming_days

            r.response_count = tbl_response.objects.filter(request_id=r).count()

            accept.append(r)

    return render(request, 'Admin/ViewRequest.html', {
        "pending": pending,
        "accept": accept,
        "reject": reject_raw
    })

def acceptrequest(request, id):
    if request.method == "POST":
        rdata = tbl_request.objects.get(id=id)
        rdata.request_status = 1
        rdata.request_message = request.POST.get("txt_message")
        rdata.save()
    return redirect('Admin:ViewRequest')


def rejectrequest(request, id):
    if request.method == "POST":
        rdata = tbl_request.objects.get(id=id)
        rdata.request_status = 2
        rdata.request_message = request.POST.get("txt_message")
        rdata.save()
    return redirect('Admin:ViewRequest')



def closerequest(request, id):
    req = tbl_request.objects.get(id=id)
    req.request_status = 2
    req.save()
    return redirect('Admin:ViewRequest')


def ViewResponse(request,id):
    responsedata=tbl_response.objects.filter(request_id=id)
    return render(request,'Admin/ViewResponse.html',{"responsedata":responsedata})

def Camp(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    else:
        campdata=tbl_camp.objects.all()
        district=tbl_district.objects.all()
        place=tbl_place.objects.all()
        if request.method=="POST":
            details=request.POST.get("txt_details")
            place=tbl_place.objects.get(id=request.POST.get('sel_place'))
            volunteerdata=tbl_volunteer.objects.get(id=request.session["vid"])

            tbl_camp.objects.create(camp_details=details,place_id=place,volunteer_id=volunteerdata)
            return redirect('Admin:Camp')
        else:
            return render(request,'Admin/Camp.html',{'district':district,'place':place,'camp':campdata})
            
def Start(request,id):
    sdata=tbl_camp.objects.get(id=id)
    sdata.camp_status=1
    sdata.save()
    return redirect('Admin:Camp')

def End(request,id):
    edata=tbl_camp.objects.get(id=id)
    edata.camp_status=2
    edata.save()
    return redirect('Admin:Camp')

def AssignVolunteer(request,id):
    volunteer = tbl_volunteer.objects.filter(volunteer_status = 1)
    return render(request,"Admin/AssignVolunteer.html",{'volunteerdata':volunteer})
def DonationRequest(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")

    requestdata = tbl_donationrequest.objects.all()
    district = tbl_district.objects.all()

    if request.method == "POST":
        details = request.POST.get("txt_details")
        place = tbl_place.objects.get(id=request.POST.get("sel_place"))
        user = tbl_user.objects.get(id=request.session["uid"])

        tbl_donationrequest.objects.create(
            donationrequest_details=details,
            place_id=place,
            user_id=user
        )
        return redirect('Admin:DonationRequest')

    return render(request,"Admin/DonationRequest.html",{
        'district':district,
        'requestdata':requestdata
    })


def AddItem(request, id):
    requestDat = tbl_donationrequest.objects.get(id=id)
    itemdata = tbl_donationitems.objects.filter(donationrequest_id=requestDat)

    if request.method == "POST":
        name = request.POST.get("txt_name")
        count = request.POST.get("txt_count")

        tbl_donationitems.objects.create(
            donationitems_name=name,
            donationitems_count=count,
            donationrequest_id=requestDat
        )
        return redirect('Admin:AddItem', id=id)

    return render(request,"Admin/AddItem.html",{
        'itemdata':itemdata,
        'id':id
    })

def Closed(request,id):
    cdata=tbl_donationrequest.objects.get(id=id)
    cdata.donationrequest_status=1
    cdata.save()
    return redirect('Admin:DonationRequest')


def delitem(request, id):
    item = tbl_donationitems.objects.get(id=id)
    rid = item.donationrequest_id.id
    item.delete()
    return redirect('Admin:AddItem', id=rid)


def delrequest(request, id):
    tbl_donationrequest.objects.get(id=id).delete()
    return redirect('Admin:DonationRequest')

def ViewDonation(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")

    viewdonationdata = tbl_donation.objects.all().prefetch_related(
        'tbl_collectionrequest_set',
        'user_id',
        'volunteer_id'
    )

    return render(request, 'Admin/ViewDonation.html', {
        'viewdonationdata': viewdonationdata
    })

def Assign(request,aid):
    district=tbl_district.objects.all()
    volunteerdata=tbl_volunteer.objects.get(id=aid)
    if request.method == "POST":
        place=tbl_place.objects.get(id=request.POST.get('sel_place'))    
        description=request.POST.get('txt_description')
        tbl_assigndonation.objects.create(volunteer_id=volunteerdata,place_id=place,assigndonation_description=description)
        return render(request,'Admin/Assign.html',{'msg':"Assigned"})
    else:
        return render(request,'Admin/Assign.html',{'district':district,'volunteerdata':volunteerdata})
    
def ViewComplaint(request):
    complaintdata=tbl_complaint.objects.all()
    return render(request,'Admin/ViewComplaint.html',{'complaintdata':complaintdata})

def Reply(request,id):
    userdata=tbl_user.objects.all()
    complaintdata=tbl_complaint.objects.get(id=id)
    if request.method == 'POST':
        reply=request.POST.get("txt_reply")
        complaintdata.complaint_reply=reply
        complaintdata.complaint_status=1
        complaintdata.save()
        return render(request,'Admin/Reply.html',{'msg':'Replied'})
    else:
        return render(request,'Admin/Reply.html',{'complaintdata':complaintdata,'userdata':userdata})
    
def SendSelectedCollection(request):
    if request.method == "POST":
        ids = request.POST.getlist("donation_ids")

        count = 0
        for did in ids:
            donation = tbl_donation.objects.get(id=did)
            if not tbl_collectionrequest.objects.filter(donation_id=donation).exists():
                tbl_collectionrequest.objects.create(donation_id=donation)
                count += 1

        viewdonationdata = tbl_donation.objects.all()
        return render(request, "Admin/ViewDonation.html", {
            "viewdonationdata": viewdonationdata,
            "msg": f"{count} Collection Requests Sent"
        })

    

def SendAllCollection(request):
    donations = tbl_donation.objects.all()
    count = 0

    for donation in donations:
        if not tbl_collectionrequest.objects.filter(donation_id=donation).exists():
            tbl_collectionrequest.objects.create(donation_id=donation)
            count += 1

    viewdonationdata = tbl_donation.objects.all()
    return render(request, "Admin/ViewDonation.html", {
        "viewdonationdata": viewdonationdata,
        "msg": f"{count} Collection Requests Sent"
    })



def ViewUserDonation(request):
    paymentdata=tbl_payment.objects.all()
    return render(request,"Admin/ViewUserDonation.html",{"paymentdata":paymentdata})

def ViewMembers(request, rid):
    memberdata = tbl_taskmember.objects.filter(
        response_id_id=rid
    )
    return render(request, "Admin/ViewMembers.html", {
        "memberdata": memberdata
    })




def DonationReport(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")

    today = date.today()

    total_amount = tbl_payment.objects.aggregate(
        total=Sum('payment_amount')
    )['total'] or 0

    today_amount = tbl_payment.objects.filter(
        payment_date=today
    ).aggregate(
        total=Sum('payment_amount')
    )['total'] or 0

    paymentdata = tbl_payment.objects.all().order_by('-payment_date')

    return render(request, "Admin/DonationReport.html", {
        "total_amount": total_amount,
        "today_amount": today_amount,
        "paymentdata": paymentdata
    })

def Awareness(request):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    
    awarenessdata = tbl_awareness.objects.all().order_by('-awareness_date')
    
    if request.method == "POST":
        title = request.POST.get("txt_title")
        description = request.POST.get("txt_description")
        image = request.FILES.get("file_image")
        
        if image:
            tbl_awareness.objects.create(
                awareness_title=title,
                awareness_description=description,
                awareness_image=image
            )
            return render(request, 'Admin/Awareness.html', {
                'msg': 'Awareness content added successfully',
                'awareness': awarenessdata
            })
        else:
            return render(request, 'Admin/Awareness.html', {
                'msg': 'Please select an image',
                'awareness': awarenessdata
            })
    else:
        return render(request, 'Admin/Awareness.html', {'awareness': awarenessdata})

def delawareness(request, id):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    tbl_awareness.objects.get(id=id).delete()
    return redirect("Admin:Awareness")

def editawareness(request, id):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    
    editdata = tbl_awareness.objects.get(id=id)
    
    if request.method == "POST":
        editdata.awareness_title = request.POST.get("txt_title")
        editdata.awareness_description = request.POST.get("txt_description")
        
        if request.FILES.get("file_image"):
            editdata.awareness_image = request.FILES.get("file_image")
        
        editdata.save()
        return redirect("Admin:Awareness")
    else:
        return render(request, 'Admin/Awareness.html', {'editdata': editdata, 'awareness': tbl_awareness.objects.all().order_by('-awareness_date')})

def toggleawareness(request, id):
    if "aid" not in request.session:
        return redirect("Guest:Login")
    
    awareness = tbl_awareness.objects.get(id=id)
    awareness.awareness_status = 1 if awareness.awareness_status == 0 else 0
    awareness.save()
    return redirect("Admin:Awareness")
