from django.db import models
from django_mysql.models import ListTextField, JSONField, ListCharField


class Scenario(models.Model):
    lookback_period = models.IntegerField()
    ticker_list = ListCharField(base_field=models.CharField(max_length=20), size=100, max_length=(20*110))
    protection_degree = models.IntegerField()
    time_flag = models.SmallIntegerField()


class InvestReport(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    invest_date = models.DateTimeField()
    invest_plan = JSONField()
    evaluate_date = models.DateTimeField()
    evaluate_revenue = models.FloatField()


