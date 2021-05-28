from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from django.views.generic import UpdateView

from . import forms


def login_view(request):
    """
    Logins the user
    """
    user = None
    form_instance = forms.LoginForm()
    if request.method == 'POST':
        form_instance = forms.LoginForm(data=request.POST)
        if form_instance.is_valid():
            username = form_instance.cleaned_data['username']
            password = form_instance.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # The user was found and authenticated
                login(request, user)
                next_url = request.GET.get('next', '/')
                # Make sure we only redirect to internal urls
                if is_safe_url(next_url, settings.ALLOWED_HOSTS):
                    return redirect(next_url)
                else:
                    return redirect('/')
            else:
                # The user or password is invalid
                messages.error(request, "Username or password was incorrect. ⁉")
    return render(
        request,
        context={
            'form': form_instance,
        },
        template_name='users/login.html'
    )


# View function
def logout_view(request):
    """
    Logs out the user
    """
    logout(request)
    messages.info(request, "You\'ve been logged out.")
    return redirect('home')


# View class
class EditUserProfile(LoginRequiredMixin, UpdateView):
    """
    Updates a user profile
    """
    model = get_user_model()
    fields = (
        'first_name',
        'last_name',
        'email'
    )
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('blog:show-all-posts')

    def get_object(self, queryset=None):
        """
        Overridden to only return current logged on user
        """
        return self.request.user
