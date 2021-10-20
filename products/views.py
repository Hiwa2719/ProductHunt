from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .forms import ProductCreateForm
from .models import Product


class IndexView(ListView):
    template_name = 'products/index.html'
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
    form_class = ProductCreateForm
    template_name = 'products/product_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.hunter = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductUpdateView(UpdateView):
    model = Product
