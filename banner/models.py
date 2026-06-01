from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(blank=True)

    image = models.ImageField(upload_to="banners/")  # Cloudinary use করলে auto cloud এ যাবে

    cta = models.CharField(max_length=100, default="Shop Now")
    href = models.CharField(max_length=255, default="/")

    accent_color = models.CharField(max_length=20, default="#ff4d4d")

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title