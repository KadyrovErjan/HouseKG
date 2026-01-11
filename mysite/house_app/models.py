from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser

USER_ROLE = (
    ('seller', 'seller'),
    ('client', 'client')
)

class UserProfile(AbstractUser):
    role = models.CharField(max_length=10, choices=USER_ROLE, default='client')
    phone_number = PhoneNumberField(default='KG', null=True, blank=True)
    LANGUAGE_TYPE = (
        ('KG', 'KG'),
        ('RU', 'RU'),
        ('EN', 'EN')
    )
    preferred_language = models.CharField(max_length=5, choices=LANGUAGE_TYPE, default='EN')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class Region(models.Model):
    region_name = models.CharField(max_length=32, unique=True)

class City(models.Model):
    city_name = models.CharField(max_length=32, unique=True)

class District(models.Model):
    district_name = models.CharField(max_length=32, unique=True)

class Property(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    PROPERTY_TYPE = (
        ('House', 'House'),
        ('FLat', 'FLat'),
        ('Plot', 'Plot'),
        ('Commercial real estate', 'Commercial real estate')
    )
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='property_region')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='property_city' )
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='property_district')
    address = models.CharField(max_length=32)
    area = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rooms = models.PositiveSmallIntegerField()
    total_floors = models.PositiveSmallIntegerField()
    CONDITION_CHOICES = (
        ('new', 'new'),
        ('renovated', 'renovated'),
        ('needs renovation', 'needs renovation'),
    )
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    image = models.ImageField(upload_to='property_image/')
    DOCUMENT_TYPE = (
        ('green book', 'green_book'),
        ('red book', 'red_book')
    )
    document = models.CharField(max_length=12, choices=DOCUMENT_TYPE)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class PropertyImages(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='all_property_image')
    property_images = models.ImageField(upload_to='property_images/')

class Floor(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='all_floors')
    number_floor = models.IntegerField()

class Review(models.Model):
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_seller')
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_buyer')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class House(models.Model):
    GrLivArea = models.IntegerField()
    YearBuilt = models.IntegerField()
    GarageCars = models.IntegerField()
    TotalBsmtSF = models.IntegerField()
    FullBath = models.IntegerField()
    OverallQual = models.IntegerField()
    Neighborhood = models.CharField(max_length=50)
    predicted_price = models.FloatField(null=True, blank=True)


    def __str__(self):
        return self.Neighborhood