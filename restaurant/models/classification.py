from django.db import models
import uuid
from django.utils.text import slugify

class RestaurantCategory(models.Model):
    """
    Represents different categories of restaurants (e.g., Fine Dining, Casual, Fast Food)
    """
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'restaurant_category'
        verbose_name = 'Restaurant Category'
        verbose_name_plural = 'Restaurant Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    @property
    def full_hierarchy(self):
        """Returns the full category hierarchy path"""
        if self.parent:
            return f"{self.parent.full_hierarchy} > {self.name}"
        return self.name


class RestaurantCuisineType(models.Model):
    """
    Represents different cuisine types (e.g., Italian, Japanese, Brazilian)
    """
    cuisine_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcuisines'
    )
    icon = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'restaurant_cuisine_type'
        verbose_name = 'Restaurant Cuisine Type'
        verbose_name_plural = 'Restaurant Cuisine Types'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name

    @property
    def full_hierarchy(self):
        """Returns the full cuisine type hierarchy path"""
        if self.parent:
            return f"{self.parent.full_hierarchy} > {self.name}"
        return self.name