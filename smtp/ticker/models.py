from django.db import models


class Ticker(models.Model):
    code = models.CharField(max_length=20)
    name = models.TextField()
    ticker = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name
