
import django_tables2 as tables

from .models import HighAlc


class HighAlcTable(tables.Table):
    class Meta:
        model = HighAlc
        sequence = ('item_name', 'profit')
        attrs = {"class": "table table-hover"}
        template_name = 'django_tables2/bootstrap.html'
        fields = ('item_name', 'profit')
