from django.db import models


class HighAlc(models.Model):
    item_name = models.CharField(max_length=100)
    profit = models.PositiveIntegerField(verbose_name=("profit"))

    class Meta:
        pass


class QuickFlips(models.Model):
    item_name = models.CharField(max_length=100, verbose_name='Item Name')
    profit = models.IntegerField(verbose_name='Item Profit')
    item_price = models.PositiveIntegerField()

    class Meta:
        pass

    def __str__(self):
        return self.item_name + str(self.profit)


class Ingredient(models.Model):
    item_name = models.CharField(max_length=100)
    item_price = models.PositiveIntegerField(default=1)
    parent_item = models.ForeignKey(QuickFlips, on_delete=models.CASCADE)
    profit = models.IntegerField()

    def __str__(self):
        return self.item_name + str(self.item_price) + str(self.parent_item) + str(self.profit)
