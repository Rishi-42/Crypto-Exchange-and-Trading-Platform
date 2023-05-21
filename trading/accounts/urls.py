from django.urls import path
from .views import *
"""
Defining the url patterns
for every views
"""
urlpatterns = [
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('resetpassword_validate/<uidb64>/<token>/',
         resetpassword_validate, name='resetpassword_validate'),
    path('forgotpassword/', forgotpassword, name="forgotpassword"),
    path('resetpassword/', resetpassword, name="resetpassword"),
    path('two_auth/', two_auth, name="two_auth"),
    path('logout', logout, name='logout'),
]
