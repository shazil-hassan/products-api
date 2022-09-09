
from django.urls import path
from .views import *

urlpatterns = [
     path('stu_signup/', StudentSignup.as_view()),
    path('stu_login/', Studentlogin.as_view()),
    path('stu_get/',StudentApi.as_view()),
    path('stu_get/<int:pk>/',StudentApi.as_view()),


]