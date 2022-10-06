from django.shortcuts import render
import datetime

import get_price
from prices.forms import ItemQuery
from .tables import HighAlcTable
from .models import HighAlc
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


def high_alc_calculator(request):
    alc = high_alc_calc.alc_profit()
    sorted_alc = high_alc_calc.sort_alc_list(alc)
    for key in sorted_alc:
        HighAlc.objects.create(item_name=key, profit=sorted_alc[key])
    table = HighAlcTable(HighAlc.objects.all())
    return render(request, 'high_alc_calc.html', {
        "table": table
    })


def quick_money(request):
    return render(request, 'quick_money.html', )
