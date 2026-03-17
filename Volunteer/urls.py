from django.urls import path,include
from Volunteer import views

app_name="Volunteer"


urlpatterns = [path("HomePage/",views.HomePage,name="HomePage"),
               path("MyProfile/",views.MyProfile,name="MyProfile"),
               path("EditProfile/",views.EditProfile,name="EditProfile"),
               path("ChangePassword/",views.ChangePassword,name="ChangePassword"),
               path("ViewRequest/",views.viewrequest,name="ViewRequest"),
               path("Join/<int:id>",views.join,name="Join"),
               path("ViewDonationRequest/",views.ViewDonationRequest,name="ViewDonationRequest"),
               path("ViewItem/<int:id>",views.ViewItem,name="ViewItem"),
               path("Donate/<int:id>",views.Donate,name="Donate"),
               path("PaymentPage/",views.PaymentPage,name="Payment"),


               path("logout/",views.logout,name="logout"),
               path("Complaint/",views.Complaint,name="Complaint"),
               path("ViewMyTask/",views.ViewMyTask,name="ViewMyTask"),
               path("Accepted/<int:id>",views.Accepted,name="Accepted"),
               path("InProgress/<int:id>",views.InProgress,name="InProgress"),
               path("Completed/<int:id>",views.Completed,name="Completed"),
               path("TakeRequest/<int:id>",views.TakeRequest,name="TakeRequest"),
               path("VolunteerCollectionRequest/",views.VolunteerCollectionRequest,name="VolunteerCollectionRequest"),
               path("MyCollectionRequest/",views.MyCollectionRequest,name="MyCollectionRequest"),
               path("updatestatus/<int:id>/<int:status>",views.updatestatus,name="updatestatus"),
               path("Team/",views.Team,name="Team"),
               path("delteam/<int:id>",views.delteam,name="delteam"),

               path("ViewMyTask/", views.ViewMyTask, name="ViewMyTask"),
                path("AssignMembers/<int:rid>/", views.AssignMembers, name="AssignMembers"),

                path('AssignCollectionMembers/<int:cid>', views.AssignCollectionMembers, name="AssignCollectionMembers"),

               path('CreateExpenseRequest/', views.CreateExpenseRequest, name='CreateExpenseRequest'),
               path('ViewMyExpenseRequests/', views.ViewMyExpenseRequests, name='ViewMyExpenseRequests'),
               ]