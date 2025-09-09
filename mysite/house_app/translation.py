from .models import Region, City, District, Property
from modeltranslation.translator import TranslationOptions,register

@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('region_name', )

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name',)

@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ('district_name',)

@register(Property)
class TranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'address')
