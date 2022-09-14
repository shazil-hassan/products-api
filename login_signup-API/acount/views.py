

from genericpath import exists
import importlib
from importlib.resources import contents
from logging import exception
from operator import contains
from re import search
from turtle import title
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import  generics

from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from .pagination import PageNumber
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.

class UserSignup(generics.CreateAPIView):
    
    serializer_class = UserSerializer
    def post(self,request,format=None):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            
            return Response({'msg':'Sign Up Successfully'})
        return Response({'msg':'InValid Information'})    



class Userlogin(APIView):
    def post(self,request,format=None):
        serializer=Userlogin_Serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
          
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'Login Successfully'})
           
        return Response({'msg':'InValid Information'})



class Product_Api(APIView,PageNumberPagination): 
    
    permission_classes=[IsAuthenticated]

    page_size =3

    def get(self,request,pk=None,format=None):
        
        id=pk
        try:

            if id is not None:
                stu=Product.objects.get(pk=id)
                serializer=ProductSerializer(stu)
                return Response(serializer.data)
            
            stu=Product.objects.all()
            if request.GET.get('title') is not None:  
                stu=stu.filter(Q(title__contains=request.GET.get('title')))

            results = self.paginate_queryset(stu, request)    
            serializer=ProductSerializer(results,many=True)
            return self.get_paginated_response(serializer.data)

        except:
            return Response("Id does not exist")  

    
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




        
       