
from django.contrib import admin
from .models import IrisPlant

@admin.register(IrisPlant)
class IrisPlantAdmin(admin.ModelAdmin):
    # Columns to show in the list
    list_display = ('species', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width')
    search_fields = ('species',)
    list_filter = ('species',)
