from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class SignupView(FormView):
    form_class = UserCreationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('login')
