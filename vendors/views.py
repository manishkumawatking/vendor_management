from rest_framework import viewsets, views, status
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.utils import timezone


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor', None)
        if vendor_id:
            queryset = queryset.filter(vendor__id=vendor_id)
        return queryset
    
    @action(detail=True, methods=['post'], url_path='acknowledge')
    def acknowledge(self, request, pk=None):
        po = self.get_object()
        po.acknowledgment_date = timezone.now()
        po.save()
        return Response({'status': 'acknowledged'})
    
class VendorPerformanceView(views.APIView):
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(performance_data, status=status.HTTP_200_OK)
