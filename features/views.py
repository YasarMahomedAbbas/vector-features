from rest_framework import viewsets
from rest_framework_gis.filters import InBBoxFilter
from .models import Feature
from .serializers import FeatureSerializer

class FeatureViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing feature instances.

    - GET /features/ - List features
    - POST /features/ - Create feature
    - GET /features/{id}/ - Retrieve feature
    - PUT /features/{id}/ - Full update
    - PATCH /features/{id}/ - Partial update
    - DELETE /features/{id}/ - Delete feature
    """
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    bbox_filter_field = 'geometry'
    filter_backends = (InBBoxFilter,)
    