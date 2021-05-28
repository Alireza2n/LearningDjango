from django import forms
from . import models


class CalcForm(forms.Form):
    """
    Form for calculator
    """
    pass


class PostForm(forms.ModelForm):
    """
    Model form for Post model
    """

    class Meta:
        model = models.Post
        fields = [
            'title',
            'content',
            'intro_image',
            'categories'
        ]
