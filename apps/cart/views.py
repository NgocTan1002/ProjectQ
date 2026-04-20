from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from apps.core.db import (
    get_cart_detail, get_cart_summary,
    upsert_cart_item, get_product_detail,
)
from apps.cart.services import CartService
 
 
class CartDetailView(TemplateView):
    template_name = "cart/detail.html"
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart    = CartService.get_or_create_cart(self.request)
        items   = get_cart_detail(str(cart.id))
        summary = get_cart_summary(str(cart.id))
        context.update({
            "cart":       cart,
            "cart_items": items,
            "subtotal":   summary["subtotal"],
            "total_items": summary["total_items"],
        })
        return context
 
 
class CartAddView(View):
 
    def post(self, request, slug=None, *args, **kwargs):
        slug       = slug or request.POST.get("product_slug")
        quantity   = int(request.POST.get("quantity", 1))
        product    = get_product_detail(slug)
 
        if not product:
            return JsonResponse({"success": False, "message": "Sản phẩm không tồn tại"}, status=404)
 
        if product["stock_status"] == "out_of_stock":
            return JsonResponse({"success": False, "message": "Sản phẩm đã hết hàng"}, status=400)
 
        cart   = CartService.get_or_create_cart(request)
        price  = product.get("sale_price") or product.get("price") or 0
        result = upsert_cart_item(str(cart.id), product["id"], quantity, price)
 
        summary = get_cart_summary(str(cart.id))
 
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "success":         True,
                "message":         f'Đã thêm "{product["name"]}" vào giỏ hàng.',
                "cart_total_items": summary["total_items"],
                "item_quantity":   result["quantity"],
                "created":         result["created"],
            })
 
        messages.success(request, f'Đã thêm "{product["name"]}" vào giỏ hàng.')
        return redirect("cart:detail")