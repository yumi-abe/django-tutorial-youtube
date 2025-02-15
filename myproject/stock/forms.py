from django import forms
from .models import Record

class CalcForm(forms.Form):
    price = forms.IntegerField(label="株価")
    quantity = forms.ChoiceField(
        label='株数',
        choices=[(i, str(i)) for i in range(100, 1100, 100)],
    )
    date = forms.DateField(
        label='注文日',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    get_month = forms.ChoiceField(
        label='権利月',
        choices=[(i, f'{i}月') for i in range(1, 13)],
    )

