from django import forms


class LoginForm(forms.Form):
    """
    The login form
    """
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
