import jwt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from .serializer import userSerialzer,DoctorSerializer
from .models import users,Doctor
from django.conf import settings
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.tokens import RefreshToken


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
    try:
        user = users.objects.get(email=email, password=password)
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful.',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)

    except users.DoesNotExist:
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

class DoctorProfileAPIView(APIView):
    uthentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  
    def post(self, request):
        try:
            user = request.user
            user_id = user.id

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

        except Exception as e:
            return Response({
                'success': False,
                'message': 'An error occurred: ' + str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    user = request.users
    return Response({'message': f'Hello, {user.email}!'}, status=status.HTTP_200_OK)