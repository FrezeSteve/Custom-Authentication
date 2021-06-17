from django.contrib.auth import views as auth_views
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.views import View


from .forms import RegisterForm, CustomAuthenticationForm


class Registration(View):
    form_class = RegisterForm
    template_name = 'accounts/registration.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Do not save to table yet
            password = form.cleaned_data['password']
            try:
                validate_password(password, user)
            except ValidationError as e:
                form.add_error('password', e)  # to be displayed with the field's errors
                return render(request, self.template_name, {'form': form})
            form.save()
            return HttpResponseRedirect(reverse('accounts:login'))

        return render(request, self.template_name, {'form': form})


class Login(auth_views.LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'

    def get_redirect_url(self):
        return reverse("blog:home")


class Logout(auth_views.LogoutView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('accounts:login'))
