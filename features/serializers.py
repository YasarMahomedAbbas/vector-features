from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Feature


class FeatureSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Feature
        geo_field = 'geometry'
        fields = ('id', 'name', 'created_at', 'updated_at')

class FeatureListSerializer(serializers.ModelSerializer):
    """ For listing features without geometry to improve performance """
    class Meta:
        model = Feature
        fields = ('id', 'name', 'created_at', 'updated_at')
