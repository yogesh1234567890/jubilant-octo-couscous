from django.urls import path
from .views import *
urlpatterns=[
    path('list',supplier_list, name='supplier-list'),
    path('create/', ProductCreateView.as_view(), name='supplier-create'),
    path('<int:pk>/update/', SupplierUpdateView.as_view(), name='supplier-update'),
    path('<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier-delete'),
    path('<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),

]