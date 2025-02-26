from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderProduct

@receiver([post_save, post_delete], sender=OrderProduct)
def update_order_total_price(sender, instance, **kwargs):
    """
    این تابع پس از ذخیره یا حذف یک OrderProduct، قیمت نهایی سفارش را به‌روز می‌کند.
    """
    order = instance.order
    order.calculate_total_price()