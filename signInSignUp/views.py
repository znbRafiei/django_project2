import jwt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import userSerialzer,DoctorSerializer
from .models import users,Doctor
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser


# Create your views here.
@api_view(["POST"])
def signUp(request):
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

    for user in serialzers.data:
        if user['email'] == email and user['password'] == password :
            payload = {'email': user['email']}
            check = True
    if check:
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({'message': 'Login successful.', 'token': token}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

class DoctorProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            email = payload.get('email')  
            user = users.objects.get(email=email)  
            user_id = user.id  

        except jwt.ExpiredSignatureError:
            return Response({'success': False, 'message': 'Token has expired.'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'success': False, 'message': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
        except users.DoesNotExist:
            return Response({'success': False, 'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        serializer = DoctorSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user_id=user_id)
            return Response({
                'success': True,
                'message': 'Doctor profile created successfully.',
                'doctor_id': serializer.data['id']
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)