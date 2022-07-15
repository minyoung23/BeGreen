from django.urls import path
from django.contrib.auth import views as auth_view
from .views import register, update, delete, password, change

app_name='accounts'
urlpatterns = [
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('update/', update, name='update'),
    path('delete/', delete, name='delete'),
    path('password/', password, name='password'),
    path('change/', change, name='change'),
]