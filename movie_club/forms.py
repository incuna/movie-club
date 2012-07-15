from django import forms

from .models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        fields = ('user', 'score')
        model = Rating

