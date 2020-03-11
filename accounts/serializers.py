from . import models
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'email', 'active', 'staff', 'is_superuser', 'admin', 'last_login', )
