from django.urls import path
from django.views.generic.detail import DetailView

from .views import *
from .models import Board

app_name = 'board'

urlpatterns = [
    path('', board_list, name='board_list'),
    path('detail/<int:pk>/',DetailView.as_view(model=Board,template_name='board/detail.html'), name='board_detail'),
    path('upload/', BoardUploadView.as_view(), name='board_upload'),
    path('delete/<int:pk>/', BoardDeleteView.as_view(), name='board_delete'),
    path('update/<int:pk>/', BoardUpdateView.as_view(), name='board_update'),
]