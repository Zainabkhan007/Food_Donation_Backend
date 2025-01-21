from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
@api_view(["POST"])
def register(request):
    
    serializer = None

    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

    if UserRegisteration.objects.filter(email=email).exists():
        return Response({"error": "Email already registered as staff."}, status=status.HTTP_400_BAD_REQUEST)
    
   
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

