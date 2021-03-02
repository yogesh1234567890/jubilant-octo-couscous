from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView,ListView
from django.forms import widgets
from django.forms import inlineformset_factory
from django.db import transaction
from django.urls import reverse_lazy
from Inventory.models import *
from .models import Sales, SalesItem, salesReturn
from .forms import *
from django.views.decorators.csrf import csrf_exempt

@login_required
def sales_list(request):
    sales=Sales.objects.all().order_by('-id')
    return render(request,'sales/sales_list.html',{'sales':sales})

class SalesCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView, ListView):
    model = Sales
    template_name = "sales/sales_form.html"
    fields = '__all__'
    success_message = "New sales successfully added."

    def get_context_data(self, **kwargs):
        self.object_list=self.get_queryset()
        data = super(SalesCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = SaleItemFormset(self.request.POST)
        else:
            data['items'] = SaleItemFormset()
            data['product'] = Product.objects.all()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        print(context)
        items = context['items']
        with transaction.atomic():
            if items.is_valid():
                items.instance = form.save(commit=False)
                for i in items:
                    prod = i.cleaned_data['product']
                    product=prod.product
                    qt=i.cleaned_data['quantity']
                    sold_item=Product.objects.get(product=product)
                    if sold_item.Quantity < qt:
                        form.errors['value']='Your entered quantity exceeds inventory quantity'
                        return self.form_invalid(form)
                    else:
                        sold_item.Quantity -=qt
                        sold_item.save()
                        form.save()
                        items.save()
        return super(SalesCreateView, self).form_valid(form)

    def get_initial(self):
        initial=super(SalesCreateView,self).get_initial()
        initial['customer']=Customer.objects.get(pk=self.kwargs['pk'])
        return initial

class CustomerAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Customer
    template_name = "sales/add_customer.html"
    fields = '__all__'
    success_message = "New Customer successfully added."


class SalesDetail(LoginRequiredMixin,DetailView):
    model = Sales
    template_name = 'sales/sales_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SalesDetail, self).get_context_data(**kwargs)
        return context

def SalesUpdateView(request, sales_id):
    sale = Sales.objects.get(id=sales_id)
    form = SaleForm(request.POST, instance=sale)
    ItemFormset = inlineformset_factory(Sales, SalesItem, form=SaleForm, extra=0)

    if request.method == 'POST':
        formset = ItemFormset(request.POST, instance=sale)

        if formset.is_valid():
            form.save()
            formset.save()
            from django.contrib import messages
            messages.success(request, 'Order successfully updated')
    else:

        form = SaleForm(instance=sale)
        formset = ItemFormset(instance=sale)

    return render(request, 'sales/sales_update.html', {'form':form, 'formset' : formset})


def sales_return_list(request):
    sales=Sales.objects.all().order_by('-id')
    return render(request,'sales/sales_return_list.html',{'sales':sales})

def existing_customer_list(request):
    sales=Customer.objects.all()
    return render(request,'sales/existing_customer.html',{'sales':sales})


class existing_sales_create(LoginRequiredMixin, SuccessMessageMixin, CreateView, ListView):
    model = Sales
    template_name = "sales/sales_form.html"
    fields = '__all__'
    success_message = "New sales successfully added."

    def get_context_data(self, **kwargs):
        self.object_list=self.get_queryset()

        data = super(existing_sales_create, self).get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = SaleItemFormset(self.request.POST)
        else:
            data['items'] = SaleItemFormset()
            data['product'] = Product.objects.all()
        # print(data)
        return data
    # def get_queryset(self):
    #     data=self.get_context_data()

    def form_valid(self, form):
        context = self.get_context_data()
        print(context)
        items = context['items']
        with transaction.atomic():
            if items.is_valid():
                items.instance = form.save(commit=False)
                for i in items:
                    prod = i.cleaned_data['product']
                    product=prod.product
                    qt=i.cleaned_data['quantity']
                    sold_item=Product.objects.get(product=product)
                    if sold_item.Quantity > qt:
                        sold_item.Quantity -= qt
                        sold_item.save()
                        form.save()
                        items.save()
                    else:
                        form.errors['value'] = 'Your entered quantity exceeds inventory quantity'
                        return self.form_invalid(form)
        return super(existing_sales_create, self).form_valid(form)

    def get_initial(self):
        initial = super(existing_sales_create, self).get_initial()
        initial['customer'] = Customer.objects.get(pk=self.kwargs['pk'])
        # print(initial)
        return initial


# def load_products(request):
#     customer = request.GET.get('sales_return_id_id')
#     print(customer)
#     customer_sale=Sales.objects.get(customer_id=customer)
#     # print(customer_sale)
#     prod = SalesItem.objects.filter(sales_id_id=customer_sale)
#     print(prod)
#     return render(request,'sales/dropdown_list_options.html',{'prod':prod})



def sales_return_view(request,pk):
    sal=Sales.objects.get(pk=pk)
    print(sal)
    prods=SalesItem.objects.filter(sales_id_id=pk)
    print(prods)
    if request.method =='POST':
        form=SaleItemReturnFormset(request.POST)
        if form.is_valid():
            form.save()
        return redirect('sales-return-list')
    if request.method =='GET':
        form=SaleItemReturnFormset(queryset=SalesItem.objects.none(),initial=[{'sales_return_id': sal}])
        customer_sale=Sales.objects.get(id=pk)
        for f in form:
            f.fields['product'].queryset = SalesItem.objects.filter(sales_id_id=customer_sale)
    return render(request,'sales/sales_return_update.html',{'items':form,'prods':prods,'sal':sal})


# ----------------------------------------------------------------------------------
#payment
#-----------------------------------------------------------------------------------

class PaymentView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Payment
    template_name = "sales/payment_form.html"
    fields = '__all__'
    success_message = "New sales successfully added."

    def get_initial(self):
        initial=super(PaymentView,self).get_initial()
        initial['sales_id']=Sales.objects.get(pk=self.kwargs['pk'])
        return initial

    def get_context_data(self, **kwargs):
        data = super(PaymentView, self).get_context_data(**kwargs)
        data['prods']=Sales.objects.get(pk=self.kwargs['pk'])
        return data


class PaymentView1(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Payment
    template_name = "sales/payment_form.html"
    fields = '__all__'
    success_message = "New sales successfully added."

    def get_context_data(self, **kwargs):
        print
        context = super(PaymentView1, self).get_context_data(**kwargs)
        context['items'] = PaymentForm()
        # context['prods']= Sales.objects.get(id=self.kwargs['pk'])
        return context

