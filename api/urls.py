from django.urls import path
from . import views

app_name= 'api'
urlpatterns = [
    # viewsからindexを読み込んで、nameをindexに
    path('index', views.admin_page, name='admin_page'),
    path('check', views.check, name='check'),
    path('stock/list', views.get_stock_list, name='get_stock_list'),
    path('stock/create', views.create_stock, name='create_stock'),
    path('stock/items/create', views.create_stock_items, name='create_stock_items'),
    path('stock/<int:pk>', views.get_stock_detail, name='get_stock_detail'),
    path('stock/update/<int:pk>', views.update_stock, name='update_stock'),
    path('stock/delete/<int:pk>', views.delete_stock, name='delete_stock'),
]