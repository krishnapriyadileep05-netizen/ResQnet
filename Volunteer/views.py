from django.shortcuts import render, redirect
from Guest.models import *
from Volunteer.models import *
from User.models import *
from datetime import date


# ---------------- LOGOUT ----------------
def logout(request):
    if "vid" in request.session:
        del request.session["vid"]
    return redirect("Guest:Login")


# ---------------- HOME ----------------
def HomePage(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")
    return render(request, 'Volunteer/HomePage.html')


# ---------------- PROFILE ----------------
def MyProfile(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    volunteerdata = tbl_volunteer.objects.get(id=request.session["vid"])
    return render(request, 'Volunteer/MyProfile.html', {"vdata": volunteerdata})


def EditProfile(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    vdata = tbl_volunteer.objects.get(id=request.session["vid"])

    if request.method == "POST":
        vdata.volunteer_name = request.POST.get('txt_name')
        vdata.volunteer_email = request.POST.get('txt_email')
        vdata.volunteer_contact = request.POST.get('txt_contact')
        vdata.volunteer_address = request.POST.get('txt_address')
        vdata.save()

        return redirect("Volunteer:MyProfile")

    return render(request, 'Volunteer/EditProfile.html', {'vdata': vdata})


# ---------------- PASSWORD ----------------
def ChangePassword(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    vdata = tbl_volunteer.objects.get(id=request.session["vid"])

    if request.method == "POST":
        old = request.POST.get('txt_password')
        new = request.POST.get('txt_new')
        retype = request.POST.get('txt_retype')

        if vdata.volunteer_password != old:
            return render(request, 'Volunteer/ChangePassword.html', {"msg": "Old password incorrect"})

        if new != retype:
            return render(request, 'Volunteer/ChangePassword.html', {"msg": "Password mismatch"})

        vdata.volunteer_password = new
        vdata.save()
        return render(request, 'Volunteer/ChangePassword.html', {"msg": "Password updated"})

    return render(request, 'Volunteer/ChangePassword.html')



def viewrequest(request):
    """
    View all Emergency/Volunteer Help requests available for volunteers to join.
    
    IMPORTANT SECURITY FILTERING:
    - Only requests with request_type=1 (Emergency/Volunteer Help) are shown to volunteers
    - Donation requests (request_type=0) are NOT displayed to volunteers
    - Volunteers can ONLY join Emergency/Volunteer Help requests
    - Donation requests are managed separately and not volunteer-based
    """
    if "vid" not in request.session:
        return redirect("Guest:Login")

    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])
    today = date.today()
    # Filter: Only show Emergency/Volunteer Help requests (request_type=1)
    # Donation requests (request_type=0) are excluded
    requests = tbl_request.objects.filter(
        request_status=1,
        request_type=1  # 1 = Emergency/Volunteer Help (only this type)
    )
    requestdata = []
    print(requests)
    for req in requests:
        req.joined = tbl_response.objects.filter(
            request_id=req,
            volunteer_id=volunteer
        ).exists()

        req.is_important = (req.request_todate - today).days <= 2
        requestdata.append(req)

    return render(request, 'Volunteer/ViewRequest.html', {
        "requestdata": requestdata
    })


def join(request, id):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    req = tbl_request.objects.get(id=id)
    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])

    if tbl_response.objects.filter(request_id=req, volunteer_id=volunteer).exists():
        return redirect("Volunteer:ViewRequest")

    tbl_response.objects.create(
        request_id=req,
        volunteer_id=volunteer
    )
    return redirect("Volunteer:ViewMyTask")


# ---------------- DONATION REQUEST ----------------
def ViewDonationRequest(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    requestdata = tbl_donationrequest.objects.all()
    return render(request, 'Volunteer/ViewDonationRequest.html', {'requestdata': requestdata})


def ViewItem(request, id):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    itemdata = tbl_donationitems.objects.filter(donationrequest_id=id)
    return render(request, 'Volunteer/ViewItem.html', {'itemdata': itemdata})


# ---------------- DONATION ----------------
def Donate(request, id):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    item = tbl_donationitems.objects.get(id=id)
    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])

    if request.method == "POST":
        dtype = request.POST.get("txt_type")
        remark = request.POST.get("txt_remark")
        amount = request.POST.get("txt_amount")

        if dtype == "Money":
            request.session["donation_data"] = {
                "donation_type": dtype,
                "donation_remark": remark,
                "donation_amount": amount,
                "volunteer_id": volunteer.id,
                "donationitem_id": item.id
            }
            return redirect("Volunteer:Payment")

        tbl_donation.objects.create(
            donation_type=dtype,
            donation_remark=remark,
            donation_amount=amount,
            volunteer_id=volunteer,
            donationitem_id=item
        )
        return render(request, 'Volunteer/Donation.html', {'msg': "Donation Success"})

    return render(request, 'Volunteer/Donation.html', {'item': item})


# ---------------- PAYMENT ----------------
def PaymentPage(request):
    donation_data = request.session.get("donation_data")

    if not donation_data:
        return redirect("Volunteer:HomePage")

    if request.method == "POST":
        tbl_donation.objects.create(
            donation_type=donation_data["donation_type"],
            donation_remark=donation_data["donation_remark"],
            donation_amount=donation_data["donation_amount"],
            volunteer_id=tbl_volunteer.objects.get(id=donation_data["volunteer_id"]),
            donationitem_id=tbl_donationitems.objects.get(id=donation_data["donationitem_id"])
        )
        del request.session["donation_data"]
        return render(request, "Volunteer/Payment_suc.html")

    return render(request, "Volunteer/Payment.html", {"donation": donation_data})


# ---------------- COMPLAINT ----------------
def Complaint(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])
    complaintdata = tbl_complaint.objects.filter(volunteer_id=volunteer)

    if request.method == "POST":
        tbl_complaint.objects.create(
            complaint_title=request.POST.get('txt_title'),
            complaint_description=request.POST.get('txt_description'),
            volunteer_id=volunteer
        )
        return redirect("Volunteer:Complaint")

    return render(request, 'Volunteer/Complaint.html', {
        'volunteerdata': volunteer,
        'complaintdata': complaintdata
    })


def ViewMyTask(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    responsedata = tbl_response.objects.filter(
        volunteer_id=request.session["vid"]
    )
    return render(request, 'Volunteer/ViewMyTask.html', {
        'responsedata': responsedata
    })


def AssignMembers(request, rid):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    response = tbl_response.objects.get(id=rid)
    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])

    teamdata = tbl_team.objects.filter(volunteer_id=volunteer)
    assigned = tbl_taskmember.objects.filter(response_id=response)

    if request.method == "POST":
        member_ids = request.POST.getlist("team_id")

        for mid in member_ids:
            team = tbl_team.objects.get(id=mid)
            if not tbl_taskmember.objects.filter(
                response_id=response, team_id=team
            ).exists():
                tbl_taskmember.objects.create(
                    response_id=response,
                    team_id=team
                )

        return redirect("Volunteer:ViewMyTask")

    return render(request, "Volunteer/AssignMembers.html", {
        "teamdata": teamdata,
        "assigned": assigned,
        "response": response
    })


def Accepted(request, id):
    tbl_response.objects.filter(id=id).update(response_status=1)
    return redirect('Volunteer:ViewMyTask')


def InProgress(request, id):
    tbl_response.objects.filter(id=id).update(response_status=2)
    return redirect('Volunteer:ViewMyTask')


def Completed(request, id):
    tbl_response.objects.filter(id=id).update(response_status=3)
    return redirect('Volunteer:ViewMyTask')


# ---------------- COLLECTION ----------------
def VolunteerCollectionRequest(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])

    requests = tbl_collectionrequest.objects.filter(
        donation_id__user_id__place__district=volunteer.place.district,
        status__lt=2  )
    
    return render(request,"Volunteer/ViewCollectionRequest.html",{'requests': requests})



def MyCollectionRequest(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])
    requests = tbl_collectionrequest.objects.filter(volunteer_id=volunteer)
    return render(request, "Volunteer/MyCollectionRequest.html", {'requests': requests})


def TakeRequest(request, id):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    req = tbl_collectionrequest.objects.get(id=id)

    if req.status == 0:
        req.volunteer_id = tbl_volunteer.objects.get(id=request.session["vid"])
        req.status = 1
        req.save()

    return redirect("Volunteer:VolunteerCollectionRequest")


def updatestatus(request, id, status):
    tbl_collectionrequest.objects.filter(id=id).update(status=status)
    return redirect("Volunteer:MyCollectionRequest")


# ---------------- TEAM ----------------
def Team(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])
    teamdata = tbl_team.objects.filter(volunteer_id=volunteer)

    if request.method == "POST":
        tbl_team.objects.create(
            team_name=request.POST.get("txt_name"),
            team_photo=request.FILES.get("file_photo"),
            team_address=request.POST.get("txt_address"),
            team_gender=request.POST.get("txt_gender"),
            team_dob=request.POST.get("txt_date"),
            team_contact=request.POST.get("txt_contact"),
            volunteer_id=volunteer
        )
        return redirect("Volunteer:Team")

    return render(request, "Volunteer/Team.html", {'teamdata': teamdata})


def delteam(request, id):
    tbl_team.objects.filter(id=id).delete()
    return redirect("Volunteer:Team")


def AssignCollectionMembers(request, cid):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    collection = tbl_collectionrequest.objects.get(id=cid)
    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])

    teamdata = tbl_team.objects.filter(volunteer_id=volunteer)
    assigned = tbl_collectionmember.objects.filter(collection_id=collection)

    if request.method == "POST":
        member_ids = request.POST.getlist("team_id")

        for mid in member_ids:
            team = tbl_team.objects.get(id=mid)

            if not tbl_collectionmember.objects.filter(
                collection_id=collection, team_id=team
            ).exists():
                tbl_collectionmember.objects.create(
                    collection_id=collection,
                    team_id=team
                )

        return redirect("Volunteer:MyCollectionRequest")

    return render(request, "Volunteer/AssignCollectionMembers.html", {
        "teamdata": teamdata,
        "assigned": assigned,
        "collection": collection
    })


# ================ EXPENSE REQUEST ================
def CreateExpenseRequest(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])

    if request.method == "POST":
        amount = request.POST.get("txt_amount")
        purpose = request.POST.get("txt_purpose")
        description = request.POST.get("txt_description", "")
        bank_details = request.POST.get("txt_bank_details", "")
        bill_file = request.FILES.get("file_bill")

        tbl_volunteer_expense_request.objects.create(
            volunteer_id=volunteer,
            expense_amount=amount,
            expense_purpose=purpose,
            expense_description=description,
            bank_details=bank_details,
            expense_bill=bill_file
        )
        return render(request, "Volunteer/ExpenseRequest.html", {"msg": "Expense request submitted successfully"})

    return render(request, "Volunteer/ExpenseRequest.html")


def ViewMyExpenseRequests(request):
    if "vid" not in request.session:
        return redirect("Guest:Login")

    volunteer = tbl_volunteer.objects.get(id=request.session["vid"])
    expense_requests = tbl_volunteer_expense_request.objects.filter(volunteer_id=volunteer).order_by('-expense_date')

    return render(request, "Volunteer/MyExpenseRequests.html", {
        "expense_requests": expense_requests
    })