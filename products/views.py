from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, View
from django.urls import reverse

from .forms import ProductCreateForm
from .models import Product


class IndexView(ListView):
    template_name = 'products/index.html'
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    form_class = ProductCreateForm
    template_name = 'products/product_form.html'
    extra_context = {'input_val': 'Create'}

    def form_valid(self, form):
        self.object = form.save(commit=False)
        user = self.request.user
        self.object.hunter = user
        self.object.save()
        self.object.vote.add(user)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductUpdateView(UpdateView):
    form_class = ProductCreateForm
    model = Product
    extra_context = {'input_val': 'Update'}

    def dispatch(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get('pk'))
        if request.user == product.hunter:
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class ProductVoteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        product = Product.objects.get(pk=pk)
        product.vote_check(request.user)
        return HttpResponseRedirect(reverse('index'))
