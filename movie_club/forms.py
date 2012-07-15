from django import forms
from django.contrib.auth.models import User

from .models import Rating


class RatingForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.exclude(username='admin'))
    score = forms.ChoiceField(choices=zip(range(1,11), range(1,11)))

    class Meta:
        fields = ('user', 'score')
        model = Rating

