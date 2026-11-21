from django import forms
from .models import Contribution

class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['title', 'description', 'category', 'location', 'date', 'hours', 'photo']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}