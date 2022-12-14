
from asyncore import write
from dataclasses import field
import email
from lib2to3.pgen2 import token
from pyexpat import model
from tkinter.tix import Tree
from unittest.util import _MAX_LENGTH
from wsgiref import validate
from zoneinfo import available_timezones
from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.response import Response
# from acount.ultis import util
from  .models import *
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields=['username','email','password','confirm_password','phone','age']
        extra_kwargs={'confirm_password':{'write_only':True}, 'password':{'write_only':True}}
    

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        return data

    def save(self):
        user = User(
            username = self.validated_data['username'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            age=self.validated_data['age']
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user


class Userlogin_Serializer(serializers.ModelSerializer):
    email=serializers.EmailField()
    class Meta:
        model=User
        fields=['email','password']



class ProductSerializer(serializers.ModelSerializer):
    availability_stock=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=['id','user','title','description','price','price_currency','image','stock','availability_stock']
    

    def get_availability_stock(self,obj):
        if obj.stock is True:
            return "stock is available"
        else:
            return "stock is not available"


    
