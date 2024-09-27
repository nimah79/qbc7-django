from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Artist


class PasswordConfirmationMixin:
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'Password fields did not match.'})

        return data


class SignUpSerializer(
    PasswordConfirmationMixin,
    serializers.ModelSerializer,
):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password2',
            'email',
            'first_name',
            'last_name',
        )
        extra_kwargs = {
            'first_name': {
                'required': True,
            },
            'last_name': {
                'required': True,
            },
        }

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class ChangePasswordSerializer(
    PasswordConfirmationMixin,
    serializers.ModelSerializer,
):
    class Meta:
        model = User
        fields = (
            'old_password',
            'password',
            'password2',
        )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )
    old_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'old_password': 'Old password is incorrect.'})

        return value

    def validate(self, data):
        data = super().validate(data)

        if data['old_password'] == data['password']:
            raise serializers.ValidationError({'password': 'Password should not be the same with old password.'})

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        user.set_password(validated_data['password'])
        user.save()

        return user


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
        extra_kwargs = {
            'first_name': {
                'required': True,
            },
            'last_name': {
                'required': True,
            },
            'email': {
                'required': True,
            },
        }

    username = serializers.CharField(required=True, validators=[])

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({'email': 'Email already taken.'})

        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({'username': 'Username already taken.'})

        return value

    def create(self, validated_data):
        user = self.context['request'].user
        user.username = validated_data['username']
        user.email = validated_data['email']
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()

        return user


class AdminChangePasswordSerializer(
    PasswordConfirmationMixin,
    serializers.ModelSerializer,
):
    class Meta:
        model = User
        fields = (
            'password',
            'password2',
        )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class AdminUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )
        extra_kwargs = {
            'first_name': {
                'required': True,
            },
            'last_name': {
                'required': True,
            },
        }

    username = serializers.CharField(required=True, validators=[])

    def validate_email(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({'email': 'Email already taken.'})

        return value

    def validate_username(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({'username': 'Username already taken.'})

        return value

    def update(self, instance, validated_data):
        instance.username = validated_data['username']
        instance.email = validated_data['email']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.save()

        return instance


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name', 'about')
