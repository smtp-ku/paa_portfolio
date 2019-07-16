from django.db import models


class Monthly(models.Model):
    price_date = models.DateTimeField()
    snp = models.FloatField()
    nasdaq = models.FloatField()
    russell = models.FloatField()
    eurostoxx = models.FloatField()
    topix = models.FloatField()
    mem = models.FloatField()
    mar = models.FloatField()
    wti_idx = models.FloatField()
    agr_idx = models.FloatField()
    silver_idx = models.FloatField()
    gold_idx = models.FloatField()
    high_yield = models.FloatField()
    igb = models.FloatField()
    ltb = models.FloatField()
    skb = models.FloatField()

    def __str__(self):
        return str(self.price_date)


class Daily(models.Model):
    price_date = models.DateTimeField()
    snp = models.FloatField()
    nasdaq = models.FloatField()
    russell = models.FloatField()
    eurostoxx = models.FloatField()
    topix = models.FloatField()
    mem = models.FloatField()
    mar = models.FloatField()
    wti_idx = models.FloatField()
    agr_idx = models.FloatField()
    silver_idx = models.FloatField()
    gold_idx = models.FloatField()
    high_yield = models.FloatField()
    igb = models.FloatField()
    ltb = models.FloatField()
    skb = models.FloatField()

    def __str__(self):
        return str(self.price_date)
