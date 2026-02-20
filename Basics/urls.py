from django.urls import path,include
from Basics import views

urlpatterns = [path('Sum/',views.Sum),
path('Calculator/',views.Calculator),
path('Largest/',views.Largest),
]
