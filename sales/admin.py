from django.contrib import admin
from .models import *
# Register your models here.


class SalesModel(admin.ModelAdmin):
    list_display = ['customer']

admin.site.register(Sales, SalesModel)
admin.site.register(SalesItem)
admin.site.register(salesReturn)
admin.site.register(Payment)


class CustomerAdmin(admin.ModelAdmin):
    list_display =['name','sale_code']

admin.site.register(Customer, CustomerAdmin)