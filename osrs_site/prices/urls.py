from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_item_price, name='Price look up'),
    path('quick/all', views.quick_flips_all, name='All Quick Flips'),
    path('quick/tables', views.quick_flips_db, name='Table view of Quick Flips'),
    path('quick/<str:item>/', views.single_table, name='Item Table'),
    path('alchemy', views.high_alc_calculator, name='High Alc Calc')
]
