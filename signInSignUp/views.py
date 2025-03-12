import jwt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import DoctorSerializer, BookingSerializer
from .models import users, Doctor, Booking
from django.conf import settings
from rest_framework.views import APIView



def generate_jwt_token(user):
    payload = {
        "email": user.email,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


@api_view(["POST"])
def signUp(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if users.objects.filter(email=email).exists():
        return Response(
            {"error": "Email is already registered."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = users.objects.create(email=email, password=password)

    return Response(
        {"message": "User signed up successfully."}, status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    try:
        user = users.objects.get(email=email, password=password)
        refresh = generate_jwt_token(user)
        return Response(
            {
                "message": "Login successful.",
                "access_token": str(refresh),
            },
            status=status.HTTP_200_OK,
        )

    except users.DoesNotExist:
        return Response(
            {"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED
        )


class DoctorProfileAPIView(APIView):

    def post(self, request):
        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return Response(
                    {"success": False, "message": "Authorization header missing"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            email = payload.get("email")
            user = users.objects.filter(email=email).first()

            if not user:
                return Response(
                    {
                        "success": False,
                        "message": "User with this email does not exist",
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )

            user_id = user.id

        except jwt.ExpiredSignatureError:
            return Response(
                {"success": False, "message": "Token has expired."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except jwt.InvalidTokenError:
            return Response(
                {"success": False, "message": "Invalid token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data = request.data
        serializer = DoctorSerializer(data=data)
        if serializer.is_valid():
            existing_doctors = Doctor.objects.filter(user_id=user_id)
            if not existing_doctors:
                serializer.save(user_id=user_id)
                return Response(
                    {
                        "success": True,
                        "message": "Doctor profile created successfully.",
                        "doctor_id": serializer.data["id"],
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {
                        "success": False,
                        "message": "You can not creat another profile doctor",
                    },
                    status=status.HTTP_201_CREATED,
                )

        return Response(
            {"success": False, "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentBookingAPIView(APIView):
    def post(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response(
                {"success": False, "message": "Authorization header missing."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            email = payload.get("email")
            user = users.objects.get(email=email)
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, users.DoesNotExist):
            return Response(
                {"success": False, "message": "Invalid or expired token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        doctor_id = request.data.get("doctor_id")
        date = request.data.get("date")
        time_slot = request.data.get("time_slot")
        
        if not doctor_id or not date or not time_slot:
            return Response(
                {"success": False, "message": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        doctor = Doctor.objects.filter(id=doctor_id).first()
        if not doctor:
            return Response(
                {"success": False, "message": "Doctor not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        existing_booking = Booking.objects.filter(
            doctor=doctor, date=date, time_slot=time_slot
        ).exists()
        if existing_booking:
            return Response(
                {"success": False, "message": "Selected time slot is already booked."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking = Booking.objects.create(
            user=user, doctor=doctor, date=date, time_slot=time_slot, status="confirmed"
        )

        serializer = BookingSerializer(booking)
        return Response(
            {
                "success": True,
                "message": "Booking confirmed!",
                "booking": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
