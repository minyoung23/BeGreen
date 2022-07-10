from django.urls import path
from .views import *

app_name='shop'

urlpatterns=[
    path('', item_in_category, name='item_all'),
    path('<slug:category_slug>/', item_in_category, name='item_in_category'),
    path('<int:id>/<item_slug>/', item_detail, name='item_detail'),
]