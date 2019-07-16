from rest_framework import serializers
from .models import Monthly, Daily


class MonthlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Monthly
        fields = (
            'id',
            'price_date',
            'snp',
            'nasdaq',
            'russell',
            'eurostoxx',
            'topix',
            'mem',
            'mar',
            'wti_idx',
            'agr_idx',
            'silver_idx',
            'gold_idx',
            'high_yield',
            'igb',
            'ltb',
            'skb'
        )


class DailySerializer(serializers.ModelSerializer):
    class Meta:
        model = Daily
        fields = (
            'id',
            'price_date',
            'snp',
            'nasdaq',
            'russell',
            'eurostoxx',
            'topix',
            'mem',
            'mar',
            'wti_idx',
            'agr_idx',
            'silver_idx',
            'gold_idx',
            'high_yield',
            'igb',
            'ltb',
            'skb'
        )
