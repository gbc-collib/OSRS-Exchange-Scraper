import django_tables2 as tables

from .models import HighAlc, QuickFlips, Ingredient


class HighAlcTable(tables.Table):
    class Meta:
        model = HighAlc
        sequence = ('item_name', 'profit')
        attrs = {"class": "table table-hover"}
        template_name = 'table.html'
        fields = ('item_name', 'profit')


class FlipsTable(tables.Table):
    class Meta:
        model = Ingredient
        exclude = ('id', 'parent_item')
        parent_item = Ingredient.parent_item
        sequence = ("item_name", "item_price", 'profit')
        attrs = {'class': 'table table-hover', 'show_footer': True}
        template_name = 'table.html'
        item_name = tables.Column(accessor='item_name')
        item_price = tables.Column(accessor='item_price')
        profit = tables.Column(accessor='profit')

    def get_bottom_pinned_data(self):
        return [
            {'item_name': self.data[0].parent_item.item_name, 'item_price': self.data[0].parent_item.item_price,
             'profit': self.data[0].profit}
        ]


class AllFlipsTable(tables.Table):
    class Meta:
        model = QuickFlips
        sequence = ("parent", "profit")
        attrs = {'class': 'table table-hover'}
        template_name = 'table.html'
        fields = ("parent", "profit")
