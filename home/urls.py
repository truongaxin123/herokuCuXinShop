from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register/success', views.register_success, name='register_success'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/#sale'), name='logout')
]

