from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from apps.core.models import TimeStampedModel, SEOModel, SlugModel, SortableModel


class Category(MPTTModel, TimeStampedModel, SEOModel, SlugModel, SortableModel):
    name = models.CharField(max_length=200, db_index=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
    )
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='categories/thumbnails/', blank=True, null=True)
    icon_class = models.CharField(max_length=100, blank=True, help_text='CSS icon class (e.g. heroicon name)')
    is_active = models.BooleanField(default=True, db_index=True)
    show_in_nav = models.BooleanField(default=True, db_index=True)

    low_stock_threshold = models.PositiveIntegerField(
    default=10,
    help_text="Ngưỡng cảnh báo sắp hết hàng cho sản phẩm thuộc category này"
    )

    class MPTTMeta:
        order_insertion_by = ['sort_order', 'name']

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories:detail', kwargs={'slug': self.slug})

    @property
    def product_count(self):
        """Count products in this category and all descendants."""
        from apps.products.models import Product
        category_ids = self.get_descendants(include_self=True).values_list('id', flat=True)
        return Product.objects.filter(category_id__in=category_ids, status='published').count()

    def get_ancestors_breadcrumb(self):
        """Return list of ancestors for breadcrumb rendering."""
        return list(self.get_ancestors(include_self=True))


class Brand(TimeStampedModel, SlugModel, SortableModel):
    """Product brand/manufacturer."""
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='brands/logos/', blank=True, null=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('categories:brand', kwargs={'slug': self.slug})