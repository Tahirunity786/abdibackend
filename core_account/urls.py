from django.urls import path
from core_account.views import pic_updater, Login, Register, Register_api, Logout, Profile, profile_update, reset_password
urlpatterns = [
    path('user/login', Login, name="Login"),
    path('user/logout', Logout, name="Logout"),
    path('user/signup', Register, name="Register" ),
    path('user/profile', Profile, name="Profile" ),
    path('user/profile/update', profile_update, name="Update" ),
    path('user/pic/update', pic_updater, name="pic" ),
    path('user/profile/pass/update', reset_password, name="passupate" ),
    path('user/signup/<str:slug>/', Register_api, name="REG-API" ),
    
]
