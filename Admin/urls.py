from django.urls import path,include

from Admin import views

app_name="Admin"


urlpatterns = [
path('HomePage/',views.HomePage,name="HomePage"),
path('AdminRegistration/',views.AdminRegistration,name="AdminRegistration"),
path('District/',views.District,name="District"),
path('deldistrict/<int:id>',views.deldistrict,name="deldistrict"),
path('editdistrict/<int:id>',views.editdistrict,name="editdistrict"),

path('Category/',views.Category,name="Category"),
path('delcategory/<int:id>',views.delcategory,name="delcategory"),
path('editcategory/<int:id>',views.editcategory,name="editcategory"),

path('AdminRegistration/',views.AdminRegistration,name="AdminRegistration"),
path('delAdminRegistration/<int:id>',views.delAdminRegistration,name="delAdminRegistration"),
path('editAdminRegistration/<int:id>',views.editAdminRegistration,name="editAdminRegistration"),

path('Place/',views.Place,name="Place"),
path('delplace/<int:id>',views.delplace,name="delplace"),
path('editplace/<int:id>',views.editplace,name="editplace"),

path('Subcategory/',views.Subcategory,name="Subcategory"),
path('delsub/<int:id>',views.delsub,name="delsub"),
path('editsub/<int:id>',views.editsub,name="editsub"),

path('UserList/',views.UserList,name="UserList"),
path('VolunteerList/',views.VolunteerList,name="VolunteerList"),
path('blockuser/<int:id>',views.blockuser,name="blockuser"),

path('acceptlist/<int:id>',views.acceptvolunteer,name="acceptlist"),
path('rejectlist/<int:id>',views.rejectvolunteer,name="rejectlist"),

path('ViewRequest/',views.viewrequest,name="ViewRequest"),
path('acceptrequest/<int:id>',views.acceptrequest,name="acceptrequest"),
path('rejectrequest/<int:id>',views.rejectrequest,name="rejectrequest"),
path('closerequest/<int:id>',views.closerequest,name="closerequest"),

path('ViewResponse/<int:id>',views.ViewResponse,name="ViewResponse"),

path("Camp/",views.Camp,name="Camp"),
path('Start/<int:id>',views.Start,name="Start"),
path('End/<int:id>',views.End,name="End"),
path('AssignVolunteer/<int:id>',views.AssignVolunteer,name="AssignVolunteer"),

path("DonationRequest/",views.DonationRequest,name="DonationRequest"),
path("delrequest/<int:id>",views.delrequest,name="delrequest"),
path("AddItem/<int:id>",views.AddItem,name="AddItem"),
path("delitem/<int:id>",views.delitem,name="delitem"),
path("Closed/<int:id>",views.Closed,name="Closed"),

path("Assign/<int:aid>/",views.Assign,name="Assign"),
path("logout/",views.logout,name="logout"),
path("ViewComplaint/",views.ViewComplaint,name="ViewComplaint"),
path("Reply/<int:id>",views.Reply,name="Reply"),
path("ViewUserDonation/",views.ViewUserDonation,name="ViewUserDonation"),


path('view-donation/', views.ViewDonation, name='ViewDonation'),
path('send-selected-collection/', views.SendSelectedCollection, name='SendSelectedCollection'),
path('send-all-collection/', views.SendAllCollection, name='SendAllCollection'),

path('ViewMembers/<int:rid>', views.ViewMembers, name='ViewMembers'),
path('DonationReport/', views.DonationReport, name='DonationReport'),

path('Awareness/', views.Awareness, name='Awareness'),
path('delawareness/<int:id>', views.delawareness, name='delawareness'),
path('editawareness/<int:id>', views.editawareness, name='editawareness'),
path('toggleawareness/<int:id>', views.toggleawareness, name='toggleawareness'),
]
