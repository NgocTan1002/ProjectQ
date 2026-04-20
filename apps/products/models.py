from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from apps.core.models import TimeStampedModel, SEOModel, SlugModel, PublishableModel, SortableModel
from apps.categories.models import Category, Brand


class Product(TimeStampedModel, SEOModel, SlugModel, PublishableModel, SortableModel):
    # ─── Identity ─────────────────────────────────────────────────────────────
    name        = models.CharField(max_length=300, db_index=True)
    sku         = models.CharField(max_length=100, unique=True, db_index=True,
                                   help_text='Mã sản phẩm duy nhất')
    part_number = models.CharField(max_length=100, blank=True, db_index=True,
                                   help_text='Mã linh kiện của nhà sản xuất')

    # ─── Phân loại ────────────────────────────────────────────────────────────
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        db_index=True,
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='products',
    )

    # ─── Giá bán ──────────────────────────────────────────────────────────────
    PRICING_FIXED   = 'fixed'
    PRICING_QUOTE   = 'quote'
    PRICING_CONTACT = 'contact'
    PRICING_CHOICES = [
        (PRICING_FIXED,   'Giá cố định'),
        (PRICING_QUOTE,   'Yêu cầu báo giá'),
        (PRICING_CONTACT, 'Liên hệ để biết giá'),
    ]
    pricing_type = models.CharField(max_length=20, choices=PRICING_CHOICES,
                                    default=PRICING_FIXED)
    price        = models.DecimalField(max_digits=15, decimal_places=0,
                                       null=True, blank=True, db_index=True,
                                       help_text='Giá niêm yết (VND)')
    sale_price   = models.DecimalField(max_digits=15, decimal_places=0,
                                       null=True, blank=True,
                                       help_text='Giá khuyến mãi (VND) — để trống nếu không có')
    min_order_qty = models.PositiveIntegerField(default=1, help_text='Số lượng đặt hàng tối thiểu')

    # ─── Tồn kho ──────────────────────────────────────────────────────────────
    STOCK_IN    = 'in_stock'
    STOCK_LOW   = 'low_stock'
    STOCK_OUT   = 'out_of_stock'
    STOCK_PRE   = 'pre_order'
    STOCK_CHOICES = [
        (STOCK_IN,  'Còn hàng'),
        (STOCK_LOW, 'Sắp hết'),
        (STOCK_OUT, 'Hết hàng'),
        (STOCK_PRE, 'Đặt trước'),
    ]
    stock_status   = models.CharField(max_length=20, choices=STOCK_CHOICES,
                                      default=STOCK_IN, db_index=True)
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    # ─── Media ────────────────────────────────────────────────────────────────
    thumbnail = models.ImageField(upload_to='products/thumbnails/', blank=True, null=True)
    thumbnail_webp = ImageSpecField(
        source='thumbnail',
        processors=[ResizeToFill(400, 400)],
        format='WEBP',
        options={'quality': 85},
    )
    thumbnail_small = ImageSpecField(
        source='thumbnail',
        processors=[ResizeToFill(200, 200)],
        format='WEBP',
        options={'quality': 80},
    )

    # ─── Nội dung ─────────────────────────────────────────────────────────────
    short_description = models.TextField(max_length=500, blank=True)
    description       = models.TextField(blank=True)
    highlights        = models.JSONField(
        default=list, blank=True,
        help_text='Danh sách tính năng nổi bật. Ví dụ: ["IP67", "RS485", "0-10V output"]',
    )

    # ─── Thông số vật lý (tách rõ từng chiều để dễ nhập) ─────────────────────
    weight     = models.DecimalField(max_digits=8, decimal_places=3,
                                     null=True, blank=True, help_text='Khối lượng (kg)')
    dim_length = models.DecimalField(max_digits=8, decimal_places=1,
                                     null=True, blank=True, help_text='Chiều dài (mm)')
    dim_width  = models.DecimalField(max_digits=8, decimal_places=1,
                                     null=True, blank=True, help_text='Chiều rộng (mm)')
    dim_height = models.DecimalField(max_digits=8, decimal_places=1,
                                     null=True, blank=True, help_text='Chiều cao (mm)')

    # ─── Flags ────────────────────────────────────────────────────────────────
    is_new        = models.BooleanField(default=False, db_index=True)
    is_bestseller = models.BooleanField(default=False, db_index=True)
    requires_quote = models.BooleanField(default=False,
                                         help_text='Bắt buộc yêu cầu báo giá, không cho thêm giỏ')

    # ─── Analytics ────────────────────────────────────────────────────────────
    view_count  = models.PositiveIntegerField(default=0)
    quote_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', '-created_at']
        indexes = [
            models.Index(fields=['status', 'category']),
            models.Index(fields=['status', 'is_featured']),
            models.Index(fields=['status', 'is_new']),
            models.Index(fields=['sku']),
            models.Index(fields=['price']),
            models.Index(fields=['stock_status', 'status']),
        ]

    def __str__(self):
        return f'{self.sku} — {self.name}'

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    @property
    def display_price(self):
        """Giá hiển thị: ưu tiên sale_price nếu có."""
        if self.pricing_type != self.PRICING_FIXED:
            return None
        return self.sale_price or self.price

    @property
    def discount_percent(self):
        """Phần trăm giảm giá so với giá gốc."""
        if self.pricing_type != self.PRICING_FIXED:
            return 0
        price = self.price
        sale = self.sale_price
        if price is None or sale is None:
            return 0
        if price <= 0 or price <= sale:
            return 0
        return int(((price - sale) / price) * 100)

    @property
    def is_in_stock(self):
        return self.stock_status in (self.STOCK_IN, self.STOCK_LOW)

    def update_stock_status(self):
        threshold = self.category.low_stock_threshold

        if self.stock_quantity <= 0:
            new_status = self.STOCK_OUT
        elif self.stock_quantity <= threshold:
            new_status = self.STOCK_LOW
        else:
            new_status = self.STOCK_IN

        Product.objects.filter(pk=self.pk).update(
            stock_status=new_status
        )
        self.stock_status = new_status

class ProductImage(TimeStampedModel, SortableModel):
    """Gallery ảnh sản phẩm. Chỉ 1 ảnh được đánh dấu is_primary."""
    product  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image    = models.ImageField(upload_to='products/gallery/')
    image_webp = ImageSpecField(
        source='image',
        processors=[ResizeToFit(800, 800)],
        format='WEBP',
        options={'quality': 85},
    )
    alt_text   = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Product Image'

    def __str__(self):
        return f'{self.product.name} — Ảnh {self.sort_order}'

    def save(self, *args, **kwargs):
        # Đảm bảo chỉ 1 ảnh is_primary mỗi sản phẩm
        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product, is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductSpecification(SortableModel):
    """
    Thông số kỹ thuật dạng key-value, phân nhóm theo group.
    Ví dụ: group='Thông số điện', key='Điện áp', value='220', unit='VAC'
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    group   = models.CharField(max_length=100, blank=True,
                               help_text='Nhóm thông số (Thông số điện, Kết nối, Môi trường...)')
    key     = models.CharField(max_length=200, help_text='Tên thông số (Điện áp, Dải đo...)')
    value   = models.CharField(max_length=500, help_text='Giá trị')
    unit    = models.CharField(max_length=50, blank=True, help_text='Đơn vị (V, A, °C, mm...)')

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Product Specification'

    def __str__(self):
        return f'{self.key}: {self.value} {self.unit}'.strip()


class ProductDocument(TimeStampedModel, SortableModel):
    """
    Tài liệu đính kèm sản phẩm (Datasheet, Manual, Certificate...).
    Dùng thay thế cho các FileField riêng lẻ trên Product.
    """
    DOC_DATASHEET     = 'datasheet'
    DOC_MANUAL        = 'manual'
    DOC_CERTIFICATION = 'certification'
    DOC_DRAWING       = 'drawing'
    DOC_SOFTWARE      = 'software'
    DOC_OTHER         = 'other'
    DOC_TYPE_CHOICES  = [
        (DOC_DATASHEET,     'Datasheet'),
        (DOC_MANUAL,        'Hướng dẫn sử dụng'),
        (DOC_CERTIFICATION, 'Chứng nhận / Certificate'),
        (DOC_DRAWING,       'Bản vẽ kích thước'),
        (DOC_SOFTWARE,      'Phần mềm / Driver'),
        (DOC_OTHER,         'Tài liệu khác'),
    ]
    product   = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='documents')
    title     = models.CharField(max_length=200)
    file      = models.FileField(upload_to='products/documents/')
    doc_type  = models.CharField(max_length=30, choices=DOC_TYPE_CHOICES, default=DOC_DATASHEET)
    file_size = models.PositiveIntegerField(null=True, blank=True, help_text='Kích thước file (bytes)')

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Product Document'

    def __str__(self):
        return f'{self.product.name} — {self.title}'


class RelatedProduct(SortableModel):
    """Liên kết sản phẩm liên quan (phụ kiện, thay thế, tương thích)."""
    RELATION_ACCESSORY   = 'accessory'
    RELATION_ALTERNATIVE = 'alternative'
    RELATION_COMPATIBLE  = 'compatible'
    RELATION_BUNDLE      = 'bundle'
    RELATION_CHOICES     = [
        (RELATION_ACCESSORY,   'Phụ kiện'),
        (RELATION_ALTERNATIVE, 'Sản phẩm thay thế'),
        (RELATION_COMPATIBLE,  'Tương thích'),
        (RELATION_BUNDLE,      'Bán kèm'),
    ]
    product       = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_products')
    related       = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_to')
    relation_type = models.CharField(max_length=30, choices=RELATION_CHOICES,
                                     default=RELATION_COMPATIBLE)

    class Meta:
        unique_together = ('product', 'related')
        ordering = ['sort_order']
        verbose_name = 'Related Product'

    def __str__(self):
        return f'{self.product.name} → {self.related.name}'