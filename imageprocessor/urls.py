from django.urls import path
from . import views


app_name = "imageprocessor"


urlpatterns = [
    path('', views.index, name="index")
]