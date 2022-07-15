from django.urls import path
from .views import *

app_name='brand'

urlpatterns=[
    path('', brand, name='brand'),
]