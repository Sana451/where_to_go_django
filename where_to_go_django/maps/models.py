from django.db import models
from django.contrib.gis.db import models as geomodels


class Place(models.Model):
    title = models.CharField(max_length=255)
    description_short = models.TextField(blank=True)
    description_long = models.TextField(blank=True)
    point = geomodels.PointField(srid=4326, null=True, blank=True)

    @property
    def lat(self):
        return self.point.y if self.point else None

    @property
    def lng(self):
        return self.point.x if self.point else None


    def __str__(self):
        return self.title

    @property
    def image_urls(self):
        """
        Явно показывает, что у Place есть связанные изображения.
        Возвращает список URL в порядке поля `order`.
        """

        return [image.url for image in self.images.all()]  # type: ignore[attr-defined]


    def to_dict(self):
        """Возвращает словарь с данными места для JSON"""
        return {
            "title": self.title,
            "placeId": f"place_{self.id}",
            "lat": float(self.lat) if self.lat is not None else None,
            "lng": float(self.lng) if self.lng is not None else None,
            "imgs": [img.image.url for img in self.images.all()],  # type: ignore[attr-defined]
            "description_short": self.description_short,
            "description_long": self.description_long,
        }


class PlaceImage(models.Model):
    place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='places/')

    def __str__(self):
        return f"{self.place.title} Image {self.image.name}"

    @property
    def url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ""
