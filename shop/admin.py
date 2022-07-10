from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
    list_display = ['item_name','slug','category','brand','item_price','item_amt','available_display','available_order','created','updated']
    list_filter = ['available_display','created','updated','category']
    prepopulated_fields = {'slug': ('item_name',)}
    list_editable = ['item_price','item_amt','available_display','available_order']


admin.site.register(Item, ItemAdmin)