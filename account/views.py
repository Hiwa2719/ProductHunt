import re
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as auth_login
from django.urls import reverse_lazy

from products.models import Product


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('login')


class LoginView(auth_login):
    def get_redirect_url(self):
        redirect_to = super().get_redirect_url()
        url_match = re.search('products/vote/[0-9]+/', redirect_to)
        if url_match:
            pk_match = re.search('[0-9]+', url_match.group())
            pk = int(pk_match.group())
            if self.request.user in Product.objects.get(pk=pk).vote.all():
                return ''
        return redirect_to
