from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken


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
