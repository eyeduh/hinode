import random

from django.contrib.auth import get_user_model, authenticate
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from users.utils import send_verification_code

from users.models import UserProfile

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True},
                        'username': {'validators': []}
                        }

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise ValidationError('Wrong Credentials!')

        token, created = Token.objects.get_or_create(user=user)

        return user

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        data['token'] = instance.auth_token.key

        return data

        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', )

    def create(self, validated_data):
        email = validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        verify_code = random.randint(11111, 99999)

        cache_key = 'login_code_{}'.format(email)
        cache.set(cache_key, verify_code, timeout=120)

        send_verification_code(user, verify_code)

        return user


class ObtainTokenSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'password', 'token')

    def create(self, validated_data):
        user = authenticate(**validated_data)

        if not user:
            raise ValidationError('Wrong credentials!')

        Token.objects.get_or_create(user=user)

        return user

    def get_token(self, obj):
        return obj.auth_token.key