
from django.urls import path
from .views import *

urlpatterns = [
     path('user_signup/', UserSignup.as_view()),
    path('user_login/', Userlogin.as_view()),
    path('products/',Product_Api.as_view()),
    path('product/<int:pk>/',Product_Api.as_view()),


    


]