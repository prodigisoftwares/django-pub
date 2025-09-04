import datetime
import os


def image_upload_to(instance, filename):
    now = datetime.datetime.now()
    path = now.strftime("images/%Y/%m/%d/%H/%M")
    return os.path.join(path, filename)
