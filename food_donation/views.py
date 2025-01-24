from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
# Create your views here.
@api_view(["POST"])
def register(request):
    
    serializer = None

    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

    if UserRegisteration.objects.filter(email=email).exists():
        return Response({"error": "Email already registered as user."}, status=status.HTTP_400_BAD_REQUEST)
    
   
    serializer = UserRegisterationSerializer(data=request.data)
    password = request.data.get('password')
    password_confirmation = request.data.get('password_confirmation')

    if password != password_confirmation:
        return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

   
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["POST"])
def login(request):

    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
       
       
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
       
 
        return Response({
            'access': access_token,
            'refresh': refresh_token,
           
            'user_id': user.id,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    return Response({
        'detail': 'Invalid credentials'
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST',])
def admin_login(request):
     username=request.data.get("username")
     password=request.data.get("password")
     if not username or not password:
        return Response({'detail': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

     user = authenticate(username=username, password=password)

     if user is None:
        return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

     if not user.is_staff:
        return Response({'detail': 'You do not have permission to access this resource.'}, status=status.HTTP_403_FORBIDDEN)

     return Response({'detail': 'Login successful!'}, status=status.HTTP_200_OK)


@api_view(["POST"])
def contactus(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
      "message": "Thank you for contacting us.",
      "data": serializer.data
 }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
def get_all_msgs(request):
      if request.method == "GET":
        contact_entries = ContactUs.objects.all()
        messages = [{"message": entry.message} for entry in contact_entries]
        
        return Response(messages, status=status.HTTP_200_OK)

