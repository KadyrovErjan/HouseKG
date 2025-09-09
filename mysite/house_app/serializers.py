from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class CustomLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']


class RegionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['region_name']

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_name']


class DistrictListSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['district_name']

class PropertyListSerializer(serializers.ModelSerializer):
    region = RegionListSerializer()
    city = CityListSerializer()
    district = DistrictListSerializer()
    class Meta:
        model = Property
        fields = ['id', 'title', 'region', 'city', 'district', 'address', 'image', 'area', 'price']


class PropertyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImages
        fields = ['property_images']


class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['number_floor']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class PropertyCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class PropertyDetailSerializer(serializers.ModelSerializer):
    region = RegionListSerializer()
    city = CityListSerializer()
    district = DistrictListSerializer()
    seller = UserProfileSimpleSerializer()
    all_property_image = PropertyImagesSerializer(read_only=True, many=True)
    all_floors = FloorSerializer(read_only=True, many=True)
    class Meta:
        model = Property
        fields = ['title', 'region', 'city', 'district', 'address', 'image', 'all_property_image', 'area', 'price', 'rooms', 'total_floors', 'all_floors',
                  'condition', 'document', 'seller', 'created_at']

class RegionDetailSerializer(serializers.ModelSerializer):
    property_region = PropertyListSerializer(many=True, read_only=True)
    class Meta:
        model = Region
        fields = ['id', 'region_name', 'property_region']

class CityDetailSerializer(serializers.ModelSerializer):
    property_city = PropertyListSerializer(many=True, read_only=True)
    class Meta:
        model = City
        fields = ['id', 'city_name', 'property_city']

class DistrictDetailSerializer(serializers.ModelSerializer):
    property_district = PropertyListSerializer(many=True, read_only=True)
    class Meta:
        model = District
        fields = ['id', 'district_name', 'property_district']

class HousePredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'





