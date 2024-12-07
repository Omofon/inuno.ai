import shortuuid
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=22,
        default=shortuuid.uuid,
        editable=False,
        unique=True,
    )
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        unique_together = ("name", "slug")
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def url(self):
        return reverse("news:articles_by_category", args=[self.slug])


class SubCategory(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=22,
        default=shortuuid.uuid,
        editable=False,
        unique=True,
    )
    parent = models.ForeignKey(
        Category,
        verbose_name="Parent Category",
        related_name="subcategories",
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255, db_index=True)

    class Meta:
        verbose_name = "Sub Category"
        verbose_name_plural = "Sub Categories"
        constraints = [
            models.UniqueConstraint(
                fields=["parent", "name"],
                name="unique_subcategory_name_per_category",
            )
        ]

    def __str__(self):
        return f"{self.parent.name} - {self.name}"


class Article(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=22,
        default=shortuuid.uuid,
        editable=False,
        unique=True,
    )
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    content = models.TextField()
    source_url = models.URLField()
    image_url = models.URLField(blank=True, null=True)
    published_date = models.DateTimeField()
    category = models.ForeignKey(
        Category, related_name="articles", on_delete=models.PROTECT
    )
    sub_category = models.ForeignKey(
        SubCategory,
        related_name="articles",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    trending = models.BooleanField(db_index=True, default=False)
    editors_pick = models.BooleanField(db_index=True, default=False)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def summary(self):
        return f"{self.content[:150]}..."
