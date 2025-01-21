from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import check_password 

class UserRegisterationSerializer(serializers.ModelSerializer):
 
   
    class Meta:
        model = UserRegisteration
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        user = None
              
        try:
            user = UserRegisteration.objects.get(email=email)
           
        except UserRegisteration.DoesNotExist:
            pass

        if user and check_password(password, user.password):  
            attrs['user'] = user
            
        else:
            raise serializers.ValidationError("Invalid email or password.")
        
        return attrs