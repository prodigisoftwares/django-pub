from django.db import models

from .utils.upload import image_upload_to


class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
