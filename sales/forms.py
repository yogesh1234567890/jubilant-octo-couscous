from django.forms import ModelForm, inlineformset_factory,modelformset_factory
from django.forms import ModelForm, inlineformset_factory,modelformset_factory
from Inventory.models import Product
from django import forms
from sales.models import Customer,Sales,SalesItem,salesReturn

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

class SalesReturnForm(ModelForm):
    class Meta:
        model = salesReturn
        fields = '__all__' 
        widgets={
            'sales_return_id': forms.HiddenInput()
        }
    
    def clean(self):
        cleaned_data=super(SalesReturnForm,self).clean()
        product=cleaned_data.get('product')
        quantity=cleaned_data.get('quantity')


SaleItemReturnFormset=modelformset_factory(salesReturn,form=SalesReturnForm,extra=1)



# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = Payment
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(PaymentForm, self).__init__(*args, **kwargs)
#         self.fields['status'].widget = forms.RadioSelect()

class PaymentForm(forms.Form):
    choices=(
        ('FullyPaid','Fully paid'),
        ('PartiallyPaid','Partially paid')
    )
    sales_id = forms.CharField(widget=forms.HiddenInput())
    total_amt = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    status = forms.ChoiceField(choices=choices)
    colors = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=choices)

    # mode