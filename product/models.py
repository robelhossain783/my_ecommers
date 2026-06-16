from django.db import models


class Category(models.Model):

    name = models.CharField(
        max_length=120
    )

    slug = models.SlugField(
        unique=True
    )

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # image = models.ImageField(upload_to="products/")
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    description = models.TextField(blank=True)

    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_new_arrivals = models.BooleanField(default=False, null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name