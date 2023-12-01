from django.contrib import admin
from .models import Mebel

class MebelAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'parse_date_time', 'description']
    list_display_links = ['id', 'parse_date_time']
    search_fields = ['id', 'price', 'parse_date_time', 'description']
    list_editable = ['price', 'description']
    list_filter = ['price', 'parse_date_time']
    
    
    
admin.site.register(Mebel, MebelAdmin)