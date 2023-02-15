from django.shortcuts import render
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableMixin, SingleTableView
import urllib

import get_price
from prices.forms import ItemQuery
from .tables import HighAlcTable, AllFlipsTable, FlipsTable
from .models import HighAlc, QuickFlips, Ingredient
import quick_money
import high_alc_calc


def search_item_price(request):
    if request.method == 'POST':  # only runs when form was filled out
        # create an instance of our form, and fill it with the POST data
        form = ItemQuery(request.POST)
        if form.is_valid():  # checks that the request was valid
            queried_data = get_price.ItemData(
                request.POST['item_id']).grab_data()  # passes string from form into grab_data to get item price
            if queried_data:
                return render(request, 'prices_page.html',
                              {'item_exists': True, 'item_data': queried_data, 'form': form})
            else:
                return render(request, 'prices_page.html', {'item_exists': False, 'form': form})
    form = ItemQuery()
    # if it makes it this far it must be GET method so pass in nothing and load template
    # initiate form to take user input
    return render(request, 'prices_page.html', {'item_exists': True, 'form': form})


def create_high_alc_data(force=False):
    if not HighAlc.objects or force:
        alc = high_alc_calc.alc_profit()
        sorted_alc = high_alc_calc.sort_alc_list(alc)
        for key in sorted_alc:
            HighAlc.objects.create(item_name=key, profit=sorted_alc[key])


def high_alc_calculator(request):
    table = HighAlcTable(HighAlc.objects.all())
    RequestConfig(request, paginate={'per_page': 15}).configure(table)

    return render(request, 'high_alc_calc.html', {
        'table': table
    }
                  )


def single_table(request, item):
    quick_money.build_profits_db(quick_money.update_flip_list())
    item = item.replace('+', ' ')
    for parent_object in QuickFlips.objects.filter(item_name=item):
        items = Ingredient.objects.filter(parent_item=parent_object.id)
        table = FlipsTable(items)
    return render(request, 'quick_money.html', {
        'tables': [table]  # Tables variable and list format is used so that the same html template can be used for all
    })


def quick_flips_all(request):
    quick_money.build_profits_db(quick_money.update_flip_list())
    tables_list = [AllFlipsTable(QuickFlips.objects.all())]
    import pdb;
    pdb.set_trace()
    return render(request, 'quick_money.html', {
        'tables': tables_list
    }
                  )


def quick_flips_db(request):
    tables_list = []
    quick_money.build_profits_db(quick_money.update_flip_list())
    for parent_object in QuickFlips.objects.all():
        # print(Ingredient.objects.filter(parent_item=parent_object.id))
        items = Ingredient.objects.filter(parent_item=parent_object.id)

        tables_list.append(FlipsTable(items))
        # total = items.annotate(Sum('item_price'))
    return render(request, 'quick_money.html', {
        'tables': tables_list,
    }
                  )
