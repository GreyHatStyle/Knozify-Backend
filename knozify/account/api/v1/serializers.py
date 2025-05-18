from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User


class GoogleAuthSerializer(serializers.Serializer):
    """
    Here is backend logic of this api.
    """
    access_token = serializers.CharField(required=True)

    def validate_access_token(self, value):
        if not value:
            raise serializers.ValidationError("Tokens not provided...")

        return value
    
    def validate(self, attrs):
        token = attrs.get('access_token')

        try:
            self.idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_AUTH.get("client_key"),
            )

            return attrs
        
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        
    
    def save(self):
        email = self.idinfo['email']
        name = self.idinfo.get('name', '')
        picture = self.idinfo.get('picture', '')

        User = get_user_model()

        try:
            user = User.objects.get(email = email)

        except User.DoesNotExist:
            user = User.objects.create_user(
                username = email.split('@')[0], # little naive trick to get name
                email = email,
                first_name = name,
            )

        
        # Generating our JWT tokens now
        refresh = RefreshToken.for_user(user)

        response = {
            "access" : str(refresh.access_token),
            "refresh" : str(refresh),
            "user": {
                "email" : user.email,
                "name" : user.get_full_name(),
                "profile": picture,
            }
        }

        return response


class GetUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['username', 'email', 'contact', 'last_login']
        # TODO: Remove fields __all__ as its not safe, its just temporarily here for making frontend dev life easier.
        fields = "__all__"
        

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type":"password"})

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name", "contact"]

        extra_kwargs = {
            "username":{"required":True},
            "password":{"required":True},
        }

    def validate_username(self, value):
        if User.objects.filter(username=value):
            raise serializers.ValidationError("This username already exists!!")
        return value
    
    def validate_email(self, value):
        """
        So that the email service providers (esp) are only from gmail, yahoo, outlook, msn or apple
        """
        valid_esp = ["gmail.com", "yahoo.com", "outlook.com", "msn.com", "apple.com"]
        user_esp = value.split("@")[-1]
        

        if user_esp not in valid_esp:
            raise serializers.ValidationError(f"Kindly use email of these ESPs only {valid_esp}")
        
        return value

    def validate_contact(self, value):
        if "+91" not in value:
            raise serializers.ValidationError("Kindly use Indian Phone number only, in this format [+91XXXXXXXXXX]")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)