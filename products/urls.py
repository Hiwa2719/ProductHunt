from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    path('create-product/', views.ProductCreateView.as_view(), name='create-product'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('update/<int:pk>/', views.ProductUpdateView.as_view(), name='product-update'),
    path('vote/<int:pk>/', views.ProductVoteView.as_view(), name='vote'),
]
