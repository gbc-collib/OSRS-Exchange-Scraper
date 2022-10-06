from django.db import models


class HighAlc(models.Model):
    item_name = models.CharField(max_length=100)
    profit = models.PositiveIntegerField(verbose_name=("profit"))

    class Meta:
        pass
    def __str__(self):
        return self.name
