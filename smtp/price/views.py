from rest_framework import viewsets, filters
from .models import Monthly, Daily
from . import serializers


class MonthlyViewSet(viewsets.ModelViewSet):
    queryset = Monthly.objects.all()
    serializer_class = serializers.MonthlySerializer
    filter_backends = [filters.OrderingFilter]
    search_fields = ['price_date']


class DailyViewSet(viewsets.ModelViewSet):
    queryset = Daily.objects.all()
    serializer_class = serializers.DailySerializer
    filter_backends = [filters.OrderingFilter]
    search_fields = ['price_date']
