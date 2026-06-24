from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile
from django.db import models
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        is_new_upload = isinstance(self.avatar.file, UploadedFile)
        if is_new_upload:
            img = Image.open(self.avatar)
            if img.height > 100 or img.width > 100:
                img.thumbnail((100, 100))
                buffer = BytesIO()
                img_format = img.format or 'JPEG'
                img.save(buffer, format=img_format)
                self.avatar = ContentFile(buffer.getvalue(), name=self.avatar.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
