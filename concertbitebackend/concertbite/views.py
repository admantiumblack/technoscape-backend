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
        return HttpResponse('you are logged in', status = 201)
    if users.exists() and bcrypt.checkpw(password.encode('utf8'), str(users[0]['password']).encode('utf8')):
        request.session['Id'] = str(users[0]['Id'])
        users = list(users.values('firstName', 'lastName', 'email'))
        return JsonResponse(users, safe=False, status = 201)
    return HttpResponse('no user found', status = 201)
    
@csrf_exempt    
@require_http_methods(['POST'])
def logout(request):
    if 'Id' in request.session:
        del request.session['Id']
        return HttpResponse('logout success')

@csrf_exempt
@require_http_methods(['POST'])
def registerUser(request, username, password, email, fullname:str):
    if User.objects.filter(Q(username=username) | 
                           Q(email=email)):
        return HttpResponse('username or email is taken')
        
    hashed_password = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
    fullname = fullname.split('+')
    firstName = fullname[0].replace('-', ' ')
    lastName = fullname[1].replace('-', ' ')
    user = User(Id=uuid4(), email=email, 
                username=username, 
                password=hashed_password.decode('utf8'),
                firstName=firstName, lastName=lastName)
    user.save()
    return HttpResponse('register success', status = 201)

@csrf_exempt
@require_http_methods(['PUT'])
def update(request, args:str):
    try:
        args = args.split('&')
        newUserInfo = {}
        for i in args:
            strings = i.split('=')
            if strings[0] == 'password':
                hashed_password = bcrypt.hashpw(strings[1].encode('utf8'),
                                                bcrypt.gensalt())
                newUserInfo[strings[0]] = hashed_password.decode('utf8')
            elif strings[0] == 'dateOfBirth':
                newUserInfo[strings[0]] = strings[1].replace('+', '/')
            else:
                newUserInfo[strings[0]] = strings[1].replace('-', '')
        user = User.objects.filter(Id=request.session['Id']).all()
        user.update(**newUserInfo)
        return HttpResponse('update success', status = 201)
    except Exception as e:
        return HttpResponse(e, status = 201)


@csrf_exempt
@require_http_methods(['POST'])
def getData(request, args):
    try:
        data = User.objects.filter(Id = request.session['Id']).values()
        values = args.split('&')
        response = list(data.values(*values))
        return JsonResponse(response, safe=False, status=2001)
    except Exception as e:
        return HttpResponse(e, status = 404)
