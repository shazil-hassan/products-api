

from importlib.resources import contents
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import  generics

from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated 

from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created





def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.

class StudentSignup(generics.CreateAPIView):
    
    serializer_class = UserSerializer
    def post(self,request,format=None):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'Sign Up Successfully'})
        return Response({'msg':'InValid Information'})    



class Studentlogin(APIView):
    def post(self,request,format=None):
        serializer=Studentlogin_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Successfully'})
           
        return Response({'msg':'InValid Information'})



class StudentApi(APIView):

    def get(self,request,pk=None,format=None):
        id=pk
        if id is not None:
            stu=Product.objects.get(pk=id)
            serializer=ProductSerializer(stu)
            return Response(serializer.data)
        stu=Product.objects.all()
        serializer=ProductSerializer(stu,many=True)
        return Response(serializer.data)


    def post(self,request,format=None):
        serializer=ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data is created'})
        else:
            return Response({'error':'Invalid Data'})    


    def put(self,request,pk,format=None):
        id = pk
        stu=Product.objects.get(pk=id)
        serializer=ProductSerializer(stu,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data is updated'})
        else:
            return Response({'error':'Invalid Data'})             


    def delete(self,request,pk,format=None):
        id = pk
        stu=Product.objects.get(pk=id)
        stu.delete()
        return Response({'msg':'Data is deleted'})