from django.db import models
import os
from PIL import Image
from django.conf import settings

class Author(models.Model):
    name = models.CharField(max_length=255)
    nacionality = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    inside_code = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField(default='Just another book.')
    language = models.CharField(max_length=50)
    publication_date = models.DateField()
    edition_date = models.DateField(blank=True, null=True)
    pages = models.PositiveIntegerField()
    size = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    edition_number = models.CharField(max_length=50, default='N/A')
    isbn = models.CharField(max_length=15)
    authors = models.ManyToManyField(Author, related_name='books')
    image = models.ImageField(upload_to='book_images/%Y/%m/', blank=True, null=True)

    @staticmethod
    def resize_image(img, new_height):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_height > new_height:
            new_width = round((new_height * original_width) / original_height)
            img_pil.resize((new_width, new_height), Image.LANCZOS).save(img_full_path, optimize=True, quality=50)
        else:
            img_pil.close()

    def save(self, *args, **kwargs):
        if not self.edition_date:
            self.edition_date = self.publication_date

        super().save(*args, **kwargs)

        max_image_size = 150
        if self.image:
            self.resize_image(self.image, max_image_size)

    def __str__(self) -> str:
        return self.title
