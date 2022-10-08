from django.db import models


class HighAlc(models.Model):
    item_name = models.CharField(max_length=100)
    profit = models.PositiveIntegerField(verbose_name=("profit"))

    class Meta:
        pass


class QuickFlips(models.Model):
    item_name = models.CharField(max_length=100)
    profit = models.IntegerField()

    class Meta:
        pass

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    item_name = models.CharField(max_length=100)
    item_price = models.PositiveIntegerField()
    parent_item = models.ForeignKey(QuickFlips, on_delete=models.CASCADE)
