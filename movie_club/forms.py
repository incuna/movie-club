from django import forms
from django.contrib.auth.models import User

from .models import Rating


class RatingForm(forms.ModelForm):
    user = forms.ChoiceField(
        choices=User.objects.exclude(username='admin').values_list('pk', 'first_name'))

    class Meta:
        fields = ('user', 'score')
        model = Rating

