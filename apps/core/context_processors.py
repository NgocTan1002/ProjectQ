"""
apps/core/context_processors.py

Inject thông tin công ty vào mọi template.
Đăng ký trong TEMPLATES → OPTIONS → context_processors trong settings.
"""

from django.conf import settings


def company(request):
    """
    Trả về dict chứa thông tin công ty được đọc từ settings (→ .env).
    Các biến này khả dụng trong toàn bộ template mà không cần truyền
    thủ công qua context trong từng view.

    Sử dụng trong template:
        {{ COMPANY_NAME }}
        {{ COMPANY_PHONE }}
        {{ COMPANY_EMAIL }}
        {{ COMPANY_ADDRESS }}
    """
    return {
        "COMPANY_NAME":    getattr(settings, "COMPANY_NAME",    "IoTech"),
        "COMPANY_ADDRESS": getattr(settings, "COMPANY_ADDRESS", ""),
        "COMPANY_PHONE":   getattr(settings, "COMPANY_PHONE",   ""),
        "COMPANY_EMAIL":   getattr(settings, "COMPANY_EMAIL",   ""),
    }
