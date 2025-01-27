from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.decorators import api_view, APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
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

     return Response({'detail': 'Login successful!','username': user.username }, status=status.HTTP_200_OK)


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
        contact = ContactUs.objects.all()
        serializer = ContactSerializer(contact,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePaymentIntentView(APIView):
    def post(self, request, *args, **kwargs):
     
        serializer = PaymentIntentSerializer(data=request.data)
        if serializer.is_valid():
            payment_id = serializer.validated_data['payment_id']
            amount = serializer.validated_data['amount']
       

            try:
            
                payment_intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency="eur",
                    payment_method=payment_id,
                    confirmation_method='manual',
                    confirm=True, 
                )

                
                return Response(
                    {'clientSecret': payment_intent.client_secret},
                    status=status.HTTP_200_OK
                )
            except stripe.error.CardError as e:
                # Handle card errors
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)