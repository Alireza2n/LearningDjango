from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
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
                login(request, user)
                return redirect('home')

    return render(
        request,
        context={
            'form': form_instance,
        },
        template_name='users/login.html'
    )


def logout(request):
    """
    Logs out the user
    """
    pass
