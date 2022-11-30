from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    property_image = PropertyImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(child=serializers.FileField(
        max_length=1000000, allow_empty_file=False, use_url=True), write_only=True)

    class Meta:
        model = Property
        fields = ['id', 'url', 'property_image', 'country', 'region', 'city', 'title', 'description', 'price', 'property_type', 'category', 'address', 'property_type',
                  'area_size', 'bedroom', 'bathroom', 'garage', 'room', 'postal_code', 'year_of_construction', 'last_renovation', 'date_posted', 'uploaded_images']

    def create(self, validated_data):
        uploaded_data = validated_data.pop("uploaded_images")
        new_property = Property.objects.create(**validated_data)
        for uploaded_item in uploaded_data:
            PropertyImage.objects.create(
                property=new_property, image=uploaded_item)
        return new_property


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_image', 'contact_info', 'about']


class UserSerializer(serializers.ModelSerializer):
    # owner_property = PropertySerializer(many=True)
    user_profile = ProfileSerializer(source='profile')
    auth_token = serializers.ReadOnlyField(source='auth_token.key')

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'user_profile', 'auth_token']

    def update(self, instance, validated_data):
        user_profile_serializer = self.fields['user_profile']
        try:
            user_profile_instance = instance.profile
        except Profile.DoesNotExist:
            user_profile_instance = Profile(user=self.context['request'].user)
        user_profile_data = validated_data.pop('profile', {})

        user_profile_serializer.update(
            user_profile_instance, user_profile_data)

        instance = super().update(instance, validated_data)

        return instance


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2',
                  'email', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': 'Password dont match'})

        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        Token.objects.create(user=user)

        user.set_password(validated_data['password'])
        user.save()

        return user
