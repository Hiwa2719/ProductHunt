from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .models import Product


class IndexView(ListView):
    template_name = 'products/index.html'
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'


class ProductUpdateView(UpdateView):
    model = Product

