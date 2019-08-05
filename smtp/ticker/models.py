from django.db import models


class Ticker(models.Model):
    code = models.CharField(max_length=20)
    name = models.TextField()
    ticker = models.CharField(max_length=20)
    isBond = models.BooleanField(default=False)
    isEnabled = models.BooleanField(default=True)
    description = models.TextField()

    def __str__(self):
        return self.name
