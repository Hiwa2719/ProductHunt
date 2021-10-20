from django.urls import path

from . import views

app_name = 'products'


urlpatterns = [
    path('create-product/', views.ProductCreateView.as_view(), name='create-product'),
]