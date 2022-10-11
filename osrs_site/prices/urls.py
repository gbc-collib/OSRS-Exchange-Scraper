from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_item_price, name='index'),
    path('quick/all', views.quick_flips_all, name='index'),
    path('quick/tables', views.quick_flips_db, name='index'),
    path('alchemy', views.high_alc_calculator, name='index')
]
