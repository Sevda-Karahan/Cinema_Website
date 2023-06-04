from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    first_name = forms.CharField(label='Ad')
    last_name = forms.CharField(label='Soyad')

    class Meta:
        model = Feedback
        fields = ('title', 'content', 'first_name', 'last_name')