from django_filters import FilterSet
from .models import  Property


class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'region': ['exact'],
            'city': ['exact'],
            'district': ['exact'],
            'area': ['gt', 'lt'],
            'price': ['gt', 'lt'],
            'condition': ['exact'],
            'document': ['exact']
        }

