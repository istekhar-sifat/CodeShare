from django import forms
from .models import SharedCode  # Ensure the model is correctly imported

class SharedCodeForm(forms.ModelForm):
    class Meta:
        model = SharedCode
        fields = '__all__'  # OR specify fields explicitly, e.g., ['text', 'pin']
