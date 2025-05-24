from account.models import User
from rest_framework import serializers


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]