from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor
from django.db.models import Avg, F, Q, Count, ExpressionWrapper, FloatField
from datetime import timedelta

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, **kwargs):
    vendor = instance.vendor
    
    # On-Time Delivery Rate
    on_time_count = PurchaseOrder.objects.filter(
        vendor=vendor, status='completed', delivery_date__lte=F('order_date') + timedelta(days=F('delivery_date'))
    ).count()
    total_completed = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    if total_completed > 0:
        vendor.on_time_delivery_rate = (on_time_count / total_completed) * 100
    else:
        vendor.on_time_delivery_rate = 0

    # Quality Rating Average
    avg_quality_rating = PurchaseOrder.objects.filter(
        vendor=vendor, status='completed', quality_rating__isnull=False
    ).aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
    vendor.quality_rating_avg = avg_quality_rating

    # Average Response Time
    avg_response_time = PurchaseOrder.objects.filter(
        vendor=vendor, acknowledgment_date__isnull=False
    ).aggregate(avg_response_time=ExpressionWrapper(Avg(F('acknowledgment_date') - F('issue_date')), output_field=FloatField()))['avg_response_time']
    if avg_response_time:
        vendor.average_response_time = avg_response_time.total_seconds() / 3600  # Convert to hours
    else:
        vendor.average_response_time = 0

    # Fulfillment Rate
    fulfilled_count = PurchaseOrder.objects.filter(
        vendor=vendor, status='completed'
    ).count()
    total_orders = PurchaseOrder.objects.filter(vendor=vendor).count()
    if total_orders > 0:
        vendor.fulfillment_rate = (fulfilled_count / total_orders) * 100
    else:
        vendor.fulfillment_rate = 0

    vendor.save()
