from django.urls import path
from .views import *

app_name = 'order'

urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('complete/', order_complete,name='order_complete'),

]