import datetime
import os

from django.db import models


def image_upload_to(instance, filename):
    now = datetime.datetime.now()
    path = now.strftime("images/%Y/%m/%d/%H/%M")
    return os.path.join(path, filename)


class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
