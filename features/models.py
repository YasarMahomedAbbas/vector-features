from django.contrib.gis.db import models

class Feature(models.Model):
    """
    Model representing a geospatial feature with geometry and name.
    """
    geometry = models.GeometryField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name