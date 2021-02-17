from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import *
from Inventory.models import Product


class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'

class SaleForm(ModelForm):
    class Meta:
        model = Sales
        fields = '__all__'

class SaleItemForm(ModelForm):
    class Meta:
        model=SalesItem
        fields=['product','quantity']


SaleItemFormset=inlineformset_factory(Sales,SalesItem, form=SaleItemForm,extra=1)

class SalesReturnForm(forms.ModelForm):
    class Meta:
        model = salesReturn
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['city'].queryset = City.objects.none()

    #     if 'country' in self.data:
    #         try:
    #             country_id = int(self.data.get('country'))
    #             self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.pk:
    #         self.fields['city'].queryset = self.instance.country.city_set.order_by('name')
