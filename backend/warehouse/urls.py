from django.urls import path
from . import views

urlpatterns = [
    path('', views.warehouse_list, name='warehouse-list'),
    path('<int:warehouse_id>/stock/', views.warehouse_stock, name='warehouse-stock'),
    path('add-stock/', views.add_stock, name='add-stock'),
    path('stock-movement/', views.record_stock_movement, name='record-stock-movement'),
    path('analytics/', views.warehouse_analytics, name='warehouse-analytics'),
]