from django.urls import path
from . import views
urlpatterns = [
    path('', views.search_item_price, name='index'),
    path('quick', views.quick_money, name='index'),
    path('alchemy', views.high_alc_calculator, name='index')
]
