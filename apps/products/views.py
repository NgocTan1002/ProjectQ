from django.http import Http404
from django.views.generic import TemplateView
from django.core.cache import cache
from apps.core.db import (
    get_products, get_product_detail,
    get_product_specs, get_product_images,
    get_related_products, get_category_tree,
)
from apps.products.tasks import increment_product_views_task


class ProductListView(TemplateView):
    template_name = "products/list.html"

    def _get_int(self, key, default=1, min_val=None, max_val=None):
        try:
            val = int(self.request.GET.get(key, default))
        except (ValueError, TypeError):
            return default
        if min_val is not None:
            val = max(min_val, val)
        if max_val is not None:
            val = min(max_val, val)
        return val

    def _get_decimal(self, key):
        from decimal import Decimal, InvalidOperation
        raw = self.request.GET.get(key, "").strip()
        if not raw:
            return None
        try:
            val = Decimal(raw)
            return val if val >= 0 else None  # giá âm vô nghĩa
        except InvalidOperation:
            return None

    def _get_bool(self, key):
        return self.request.GET.get(key, "").lower() in ("1", "true", "yes")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        limit  = 24
        page   = self._get_int("page", default=1, min_val=1)
        offset = (page - 1) * limit

        products, total = get_products(
            category_id = self.request.GET.get("category") or None,
            brand_id    = self.request.GET.get("brand") or None,
            min_price   = self._get_decimal("min_price"),
            max_price   = self._get_decimal("max_price"),
            stock_only  = self._get_bool("in_stock"),
            search      = self.request.GET.get("q") or None,
            sort_by     = self.request.GET.get("sort", "featured"),
            limit       = limit,
            offset      = offset,
        )

        total_pages = (total + limit - 1) // limit

        page = min(page, total_pages) if total_pages else 1

        categories = cache.get_or_set(
            "sidebar_category_tree",
            lambda: get_category_tree(active_only=True),
            timeout=900,
        )

        context.update({
            "products":     products,
            "total":        total,
            "page":         page,
            "total_pages":  total_pages,
            "has_previous": page > 1,
            "has_next":     page < total_pages,
            "prev_page":    page - 1,
            "next_page":    page + 1,
            "categories":   categories,
            "current_sort": self.request.GET.get("sort", "featured"),
        })
        return context
 
 
class ProductDetailView(TemplateView):
    template_name = "products/detail.html"
 
    def get(self, request, slug, *args, **kwargs):
        self.slug = slug
        response = super().get(request, *args, **kwargs)

        product = self._get_product()
        if product:
            increment_product_views_task.delay(product["id"])
        return response
 
    def _get_product(self):
        cache_key = f"product_detail_{self.slug}"
        product = cache.get(cache_key)
        if not product:
            product = get_product_detail(self.slug)
            if product:
                cache.set(cache_key, product, 300)
        return product
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self._get_product()
 
        if not product:
            raise Http404("Sản phẩm không tồn tại")
 
        product_id = product["id"]
 
        # Lấy dữ liệu từ các DB functions song song
        specs    = get_product_specs(product_id)
        images   = get_product_images(product_id)
        related  = get_related_products(product_id, limit=6)
 
        specs_grouped = {}
        for s in specs:
            specs_grouped.setdefault(s["spec_group"], []).append(s)
 
        context.update({
            "product":       product,
            "specs_grouped": specs_grouped,
            "images":        images,
            "related":       related,
        })
        return context