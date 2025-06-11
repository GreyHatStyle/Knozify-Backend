from account.models import User
from rest_framework import serializers


class GetUserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['username', 'email', 'phone_no', 'last_login']
        # TODO: Remove fields __all__ as its not safe, its just temporarily here for making frontend dev life easier.
        fields = ['username', 'email', 'phone_no', 'last_login', 'age']
        