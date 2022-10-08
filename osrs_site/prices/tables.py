
import django_tables2 as tables

from .models import HighAlc, QuickFlips


class HighAlcTable(tables.Table):
    class Meta:
        model = HighAlc
        sequence = ('item_name', 'profit')
        attrs = {"class": "table table-hover"}
        template_name = 'table.html'
        fields = ('item_name', 'profit')

class QuickFlipsTable(tables.Table):
    class Meta:
        model = QuickFlips
        sequence = ("parent", "ingredient", "profit")
        attrs = {'class': 'table table-hover'}
        template_name = 'table.html'
        fields = ("parent", "ingredient", "profit")

