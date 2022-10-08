from django.contrib import admin
from .models import HighAlc, QuickFlips


@admin.register(HighAlc)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HighAlc._meta.get_fields()]
