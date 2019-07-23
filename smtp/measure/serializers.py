from rest_framework import serializers
from .models import Scenario, InvestReport


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = '__all__'


class InvestReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestReport
        fields = '__all__'
