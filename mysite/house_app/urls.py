from .views import *
from rest_framework import routers
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'review', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('', PropertyListAPIView.as_view(), name='property_list'),
    path('<int:pk>/', PropertyDetailAPIView.as_view(), name='property_detail'),
    path('property/create/', PropertyCreateAPIView.as_view(), name='property_create'),
    path('property/create/<int:pk>', PropertyEditAPIView.as_view(), name='property_edit'),
    path('region', RegionLisAPIView.as_view(), name='region_list'),
    path('region/<int:pk>/', RegionDetailAPIView.as_view(), name='region_detail'),
    path('city', CityListAPIView.as_view(), name='city_list'),
    path('city/<int:pk>/', CityDetailAPIView.as_view(), name='city_detail'),
    path('district', DistrictListAPIView.as_view(), name='district_list'),
    path('district/<int:pk>/', DistrictDetailAPIView.as_view(), name='district_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),

    path('predict/', PredictPrice.as_view(), name='predict_price'),

]