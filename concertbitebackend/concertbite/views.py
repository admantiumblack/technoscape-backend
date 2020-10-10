from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import User
from rest_framework.response import Response
from django.views.decorators.http import require_http_methods
import json
from django.db.models import Q
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt
import bcrypt

# Create your views here.
@csrf_exempt
@require_http_methods(['POST'])
def login(request, username, password):
    users = User.objects.filter(username=username,
        ).values('Id', 'firstName', 'lastName', 'email', 'password')
    if 'Id' in request.session:
        return HttpResponse('you are logged in')
    if users.exists() and bcrypt.checkpw(password.encode('utf8'), str(users[0]['password']).encode('utf8')):
        request.session['Id'] = str(users[0]['Id'])
        users = list(users.values('firstName', 'lastName', 'email'))
        return JsonResponse(users, safe=False, status = 201)
    return HttpResponse('no user found')
    
@csrf_exempt    
@require_http_methods(['POST'])
def logout(request):
    if 'Id' in request.session:
        del request.session['Id']
        return HttpResponse('logout success')

@csrf_exempt
@require_http_methods(['POST'])
def registerUser(request, username, password, email):
    if User.objects.filter(Q(username=username) | 
                           Q(email=email)):
        return HttpResponse('username or email is taken')
        
    hashed_password = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
    user = User(Id=uuid4(), email=email, username=username, password=hashed_password.decode('utf8'))
    user.save()
    return HttpResponse('register success', status = 201)