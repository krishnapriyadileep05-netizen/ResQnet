from django.urls import path,include
from Guest import views
app_name="Guest"


urlpatterns = [path('UserRegistration/',views.UserRegistration,name="UserRegistration"),
               path('Login/',views.Login,name="Login"),
               path('AjaxPlace/',views.AjaxPlace,name="ajaxplace"),
               path('Volunteer/',views.Volunteer,name="Volunteer"),
               path('',views.indexpage,name="indexpage"),
                ]