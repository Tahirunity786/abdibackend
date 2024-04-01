from django.urls import path
from core_account.views import Login, Register, Register_api, Logout, Profile
urlpatterns = [
    path('user/login', Login, name="Login"),
    path('user/logout', Logout, name="Logout"),
    path('user/signup', Register, name="Register" ),
    path('user/profile', Profile, name="Profile" ),
    path('user/signup/<str:slug>/', Register_api, name="REG-API" ),
    
]
