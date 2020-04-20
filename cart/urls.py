from django.urls import path
from . import views

app_name ='cart'


urlpatterns = [
    path('remove/<product_id>/', views.CartRemove, name='CartRemove'),
    path('add/<product_id>/', views.CartAdd, name='CartAdd'),
    path('cart/', views.CartDetail, name='CartDetail'),
]