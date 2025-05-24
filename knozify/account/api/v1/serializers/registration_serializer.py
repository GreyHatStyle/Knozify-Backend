from account.models import User
from rest_framework import serializers


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