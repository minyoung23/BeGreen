from django.urls import path
from .views import *

app_name='cart'

urlpatterns=[
    path('', detail, name='detail'),
    path('add/<int:item_id>', add, name='item_add'),
    path('remove/<item_id>', remove, name='item_remove'),
]