from django.db import models


class Ticker(models.Model):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    ticker = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name


class MonthlyPrice(models.Model):
    price_date = models.DateTimeField()
    snp = models.FloatField(default=0)
    nasdaq = models.FloatField(default=0)
    russell = models.FloatField(default=0)
    eurostoxx = models.FloatField(default=0)
    topix = models.FloatField(default=0)
    mem = models.FloatField(default=0)
    mar = models.FloatField(default=0)
    wti_idx = models.FloatField(default=0)
    agr_idx = models.FloatField(default=0)
    silver_idx = models.FloatField(default=0)
    gold_idx = models.FloatField(default=0)
    high_yield = models.FloatField(default=0)
    igb = models.FloatField(default=0)
    ltb = models.FloatField(default=0)
    skb = models.FloatField(default=0)
