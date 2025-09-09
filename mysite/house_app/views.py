from sklearn.neighbors import NeighborhoodComponentsAnalysis

from .serializers import *
from .models import *
from .permissions import *
from .pagination import PropertyPagination
from rest_framework import status, viewsets, generics, views
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from .filters import PropertyFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import os
from django.conf import settings
import joblib

model_path = os.path.join(settings.BASE_DIR, 'model.pkl')
model = joblib.load(model_path)

scaler_path = os.path.join(settings.BASE_DIR, 'scaler.pkl')
scaler = joblib.load(scaler_path)

Neighborhood = ['Blueste', 'BrDale', 'BrkSide', 'ClearCr', 'CollgCr', 'Crawfor', 'Edwards',
                'Gilbert', 'IDOTRR', 'MeadowV', 'Mitchel', 'NAmes', 'NPkVill', 'NWAmes',
                'NoRidge', 'NridgHt', 'OldTown', 'SWISU', 'Sawyer', 'SawyerW', 'Somerst',
                'StoneBr', 'Timber', 'Veenker']



class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomLoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)

# class LogoutView(generics.GenericAPIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             refresh_token = request.data['refresh']
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSimpleSerializer

class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [UserEdit]

class RegionLisAPIView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionListSerializer

class RegionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionDetailSerializer

class CityListAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializer

class CityDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer

class DistrictListAPIView(generics.ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictListSerializer

class DistrictDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictDetailSerializer

class PropertyListAPIView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializer
    pagination_class = PropertyPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PropertyFilter
    search_fields = ['title']
    ordering_fields = ['area', 'price']

class PropertyDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckUserSeller, MethodCheck]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, CheckUserBuyer]

class PropertyCreateAPIView(generics.CreateAPIView):
    serializer_class = PropertyCreateSerializers
    permission_classes = [permissions.IsAuthenticated, CheckUserSeller]

class PropertyEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyCreateSerializers
    permission_classes = [permissions.IsAuthenticated, CheckUserSeller, CheckPropertyEdit]

class PredictPrice(views.APIView):
    def post(self, request):
        serializer = HousePredictSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            new_neighborhood = data.get('Neighborhood')
            neighborhood1_0 = [1 if new_neighborhood == name else 0 for name in Neighborhood]

            features = [data['GrLivArea'],
                        data['YearBuilt'],
                        data['GarageCars'],
                        data['TotalBsmtSF'],
                        data['FullBath'],
                        data['OverallQual'],
                        ] + neighborhood1_0
            scaled_data = scaler.transform([features])
            pred = model.predict(scaled_data)[0]
            house = serializer.save(predicted_price=pred)
            return Response({'Predict Price': round(pred),
                             'data': HousePredictSerializer(house).data}, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



