# listings/forms.py
from django import forms
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
class ItemQuery(forms.Form):
		item_id = forms.CharField(required=True)
