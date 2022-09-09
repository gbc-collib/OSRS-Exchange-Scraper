from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
import get_price
from prices.forms import ItemQuery
import datetime

def search_item_price(request):
	if request.method == 'POST': #only runs when form was filled out
		# create an instance of our form, and fill it with the POST data
		form = ItemQuery((request.POST))
		if form.is_valid(): #checks that the request was valid
			quieried_data = get_price.item_data(request.POST['item_id']).grab_data() #passes string from form into grab_data to get item price
			time_retrieved = datetime.datetime.now()
			if quieried_data:
				return render(request, 'prices_page.html', {'item_exists': True, 'item_data': quieried_data, 'form': form})
			else:
				return render(request, 'prices_page.html', {'item_exists': False, 'form': form})
	form = ItemQuery()
	#if it makes it this far it must be GET method so pass in nothing and load template
	#initiate form to take user input
	#time_retrieved.strftime("%H:%M:%S"))
	return render(request, 'prices_page.html', {'item_exists': True, 'form': form})
