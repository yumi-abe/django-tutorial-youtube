from django import forms

class CalcForm(forms.Form):
    price = forms.IntegerField(label="株価")
    quantity = forms.ChoiceField(
        label='株数',
        choices=[(i, str(i)) for i in range(100, 1100, 100)],
        widget=forms.Select(attrs={'class': 'input-field'})
    )
    date = forms.DateField(
        label='注文日',
        widget=forms.DateInput(attrs={'class': 'input-field', 'type': 'date'})
    )
    get_month = forms.ChoiceField(
        label='権利月',
        choices=[(i, f'{i}月') for i in range(1, 13)],
        widget=forms.Select(attrs={'class': 'input-field month'})
    )