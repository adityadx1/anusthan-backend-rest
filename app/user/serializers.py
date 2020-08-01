from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """serializer for the user_model"""

    class Meta:
        model = get_user_model()
        fields = [
            'userid',
            'firstname',
            'middlename',
            'lastname',
            'phonenumber',
            'emailid',
            'dob',
            'gender',
            'firebaseuserid'
        ]

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        user = super().update(instance, validated_data)
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    firebaseuserid = serializers.CharField()

    def validate(self, attrs):
        """Validate and authenticate the user"""
        User = get_user_model()
        try:
            userobj = User.objects.get(
                firebaseuserid=attrs.get('firebaseuserid'))
            Token.objects.create(user=userobj)
        except User.DoesNotExist:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = userobj
        return attrs
