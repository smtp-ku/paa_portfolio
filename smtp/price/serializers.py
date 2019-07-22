from rest_framework import serializers
from .models import Monthly, Daily, Compat


class CompatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compat
        fields = '__all__'


class MonthlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Monthly
        fields = '__all__'


class DailySerializer(serializers.ModelSerializer):
    class Meta:
        model = Daily
        fields = '__all__'

