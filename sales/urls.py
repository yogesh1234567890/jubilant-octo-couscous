from django.urls import path
from .views import *

urlpatterns=[
path('',sales_list,name='sales-list'),
path('create/<int:pk>',SalesCreateView.as_view(),name='sales-create'),
path('create-sale/', CustomerAddView.as_view(), name='sale-item'),
path('sale-detail/<int:pk>',SalesDetail.as_view(), name='sales_details'),
path('<int:sales_id>/update/', SalesUpdateView, name='sales-update'),
path('return/',sales_return_list,name='sales-return-list'),
path('existing/',existing_customer_list,name='existing-customer-list'),
path('exist/create/<int:pk>',existing_sales_create.as_view(),name='existing-sales-create'),
# path('ajax/load-products/',load_products, name='ajax_load_products'),  # AJAX
path('sales-return/<int:pk>/',sales_return_view,name='salesreturn'),
path('payment/<int:pk>',PaymentView.as_view(),name='payment-create'),
path('payment/',PaymentView1.as_view(),name='payment-create1'),




]