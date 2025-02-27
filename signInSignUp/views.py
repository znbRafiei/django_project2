import jwt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import userSerialzer
from .models import users
from django.conf import settings


# Create your views here.
@api_view(["POST"])
def signUp(request):
    # all_user = users.objects.all()
    # serialzers = userSerialzer(all_user, many=True)
    # return Response(serialzers.data)
    email = request.data.get('email')
    password = request.data.get('password')
    if users.objects.filter(email=email).exists():
        return Response({'error': 'Email is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

    user = users.objects.create(
        email=email,
        password=password  
    )

    return Response({'message': 'User signed up successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    all_user = users.objects.all()
    serialzers = userSerialzer(all_user, many=True)
    # payload = {}
    # user = authenticate(request, email=email, password=password)
    # if user is not None:
    for user in serialzers.data:
        if user['email'] == email and user['password'] == password :
            payload = {'email': user['email']}
            check = True
    # if any(user['email'] == email and user['password'] == password for user in serialzers.data):
    if check:
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({'message': 'Login successful.', 'token': token}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)