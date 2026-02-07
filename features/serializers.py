from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Feature


class FeatureSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Feature
        geo_field = 'geometry'
        fields = ('id', 'name', 'created_at', 'updated_at')
