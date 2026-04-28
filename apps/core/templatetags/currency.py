from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def vnd(value):
    """
    Định dạng số tiền theo chuẩn VND Việt Nam:
      - Dấu phân cách nghìn: dấu chấm '.'
      - Không có phần thập phân
      - Hậu tố: ' ₫'
    Ví dụ: 1490000 → '1.490.000 ₫'
    """
    if value is None or value == '':
        return 'Liên hệ'
    try:
        amount = int(Decimal(str(value)))
    except (ValueError, TypeError):
        return 'Liên hệ'
    if amount == 0:
        return 'Miễn phí'
    formatted = f'{amount:,}'.replace(',', '.')
    return f'{formatted} ₫'
