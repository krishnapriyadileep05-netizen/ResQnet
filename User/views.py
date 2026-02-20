from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *
from User.models import *
from Volunteer.models import *
from Admin.models import tbl_awareness


def logout(request):
    if "uid" in request.session:
        del request.session["uid"]
    return redirect("Guest:Login")


def HomePage(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    return render(request,'User/HomePage.html')


def MyProfile(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    userdata=tbl_user.objects.get(id=request.session["uid"])
    return render(request,'User/MyProfile.html',{"userdata":userdata})


def EditProfile(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    userdata=tbl_user.objects.get(id=request.session["uid"])
    if request.method=="POST":
        userdata.user_name=request.POST.get("txt_name")
        userdata.user_email=request.POST.get("txt_email")
        userdata.user_contact=request.POST.get("txt_contact")
        userdata.user_address=request.POST.get("txt_address")
        userdata.save()
        return redirect("User:MyProfile")
    return render(request,'User/EditProfile.html',{"userdata":userdata})


def ChangePassword(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    userdata=tbl_user.objects.get(id=request.session["uid"])
    if request.method=="POST":
        if userdata.user_password!=request.POST.get("txt_old"):
            return render(request,'User/ChangePassword.html',{"msg":"Incorrect Password"})
        if request.POST.get("txt_new")!=request.POST.get("txt_retype"):
            return render(request,'User/ChangePassword.html',{"msg":"Mismatch"})
        userdata.user_password=request.POST.get("txt_new")
        userdata.save()
        return render(request,'User/ChangePassword.html',{"msg":"Updated"})
    return render(request,'User/ChangePassword.html')


def Complaint(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    userdata=tbl_user.objects.get(id=request.session["uid"])
    if request.method=="POST":
        tbl_complaint.objects.create(
            complaint_title=request.POST.get("txt_title"),
            complaint_description=request.POST.get("txt_description"),
            user_id=userdata
        )
        return redirect("User:Complaint")
    return render(request,'User/Complaint.html')


def Request(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    district = tbl_district.objects.all()
    requestdata = tbl_request.objects.filter(user_id=request.session["uid"])
    if request.method == "POST":
        req_type = int(request.POST.get("req_type"))  
        tbl_request.objects.create(
            request_title=request.POST.get("txt_title"),
            request_content=request.POST.get("txt_content"),
            request_todate=request.POST.get("txt_date"),
            request_type=req_type,
            place_id=tbl_place.objects.get(id=request.POST.get("sel_place")),
            user_id=tbl_user.objects.get(id=request.session["uid"])
        )
        return redirect("User:MyRequest")
    return render(request, 'User/request.html', {'district': district,'requestdata': requestdata})

def ViewDonationRequest(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    requestdata=tbl_donationrequest.objects.filter(donationrequest_status=0)
    return render(request,'User/ViewDonationRequest.html',{'requestdata':requestdata})

def ViewItem(request,id):
    itemdata=tbl_donationitems.objects.filter(donationrequest_id=id)
    return render(request,'User/ViewItem.html',{'itemdata':itemdata})

def Donate(request,id):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    item=tbl_donationitems.objects.get(id=id)
    userdata=tbl_user.objects.get(id=request.session["uid"])
    if request.method=="POST":
        dtype=request.POST.get("txt_type")
        remark=request.POST.get("txt_remark")
        amount=request.POST.get("txt_amount")
        if dtype=="Money":
            request.session["donation_data"]={
                "donation_type":dtype,
                "donation_remark":remark,
                "donation_amount":amount,
                "user_id":userdata.id,
                "donationitem_id":item.id
            }
            return redirect("User:Payment")
        tbl_donation.objects.create(
            donation_type=dtype,
            donation_remark=remark,
            donation_amount=amount,
            user_id=userdata,
            donationitem_id=item
        )
        return redirect("User:HomePage")
    return render(request,'User/Donate.html',{'item':item})


def PaymentPage(request):
    donation_data=request.session.get("donation_data")
    if not donation_data:
        return redirect("User:HomePage")
    if request.method=="POST":
        tbl_donation.objects.create(
            donation_type=donation_data["donation_type"],
            donation_remark=donation_data["donation_remark"],
            donation_amount=donation_data["donation_amount"],
            user_id=tbl_user.objects.get(id=donation_data["user_id"]),
            donationitem_id=tbl_donationitems.objects.get(id=donation_data["donationitem_id"])
        )
        del request.session["donation_data"]
        return render(request,"User/Payment_suc.html")
    return render(request,"User/Payment.html",{"donation":donation_data})


def ViewCamp(request):
    campdata=tbl_camp.objects.all()
    return render(request,"User/ViewCamp.html",{'campdata':campdata})


def Feedback(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    userdata=tbl_user.objects.get(id=request.session["uid"])
    if request.method=="POST":
        tbl_feedback.objects.create(
            feedback_content=request.POST.get("txt_content"),
            user_id=userdata
        )
        return redirect("User:Feedback")
    return render(request,'User/Feedback.html')

def MyRequest(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")

    userdata = tbl_user.objects.get(id=request.session["uid"])
    requestdata = tbl_request.objects.filter(user_id=userdata)

    return render(request, "User/MyRequest.html", {
        "requestdata": requestdata
    })

def ViewMembers(request, rid):
    volunteers = tbl_response.objects.filter(
        request_id_id=rid
    ).select_related("volunteer_id")

    taskmembers = tbl_taskmember.objects.filter(
        response_id__request_id_id=rid
    ).select_related("team_id", "response_id")

    return render(request, "User/ViewMembers.html", {
        "volunteers": volunteers,
        "taskmembers": taskmembers
    })

def ViewAwareness(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    
    # Get only active awareness content
    awarenessdata = tbl_awareness.objects.filter(awareness_status=0).order_by('-awareness_date')
    
    return render(request, 'User/ViewAwareness.html', {'awareness': awarenessdata})



def DirectDonation(request):
    if "uid" not in request.session:
        return redirect("Guest:Login")
    userdata = tbl_user.objects.get(id=request.session["uid"])
    if request.method == "POST":
        amount = request.POST.get("txt_amount")
        tbl_payment.objects.create(
            payment_amount= amount,
            user_id=userdata
        )
        return render(request,"User/Payment_suc.html")
    return render(request, "User/DirectDonation.html")