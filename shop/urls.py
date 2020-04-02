from django.urls import path
from . import views

app_name ='shop'

urlpatterns = [
    path('<str:category_slug>/', views.ProductList, name='ProductListByCategory'),
    path('<int:id>/<slug:slug>/', views.ProductDetail, name='ProductDetail'),
    path('', views.ProductList, name='ProductList'),
]

