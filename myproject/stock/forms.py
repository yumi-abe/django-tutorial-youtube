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

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field'}),
            'get_date': forms.DateInput(attrs={'type': 'date', 'class': 'input-field'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date', 'class': 'input-field'}),
            'label': forms.Select(attrs={'class': 'input-field'}),  # 修正：ChoiceField -> Select
            'code': forms.TextInput(attrs={'class': 'input-field'}),
            'stock_name': forms.TextInput(attrs={'class': 'input-field'}),
            'get_month': forms.Select(attrs={'class': 'input-field'}),
            'quantity': forms.Select(attrs={'class': 'input-field'}),
            'stock_price': forms.NumberInput(attrs={'class': 'input-field'}),
            'fee': forms.NumberInput(attrs={'class': 'input-field'}),
            'category': forms.Select(attrs={'class': 'input-field'}),
            'detail': forms.TextInput(attrs={'class': 'input-field'}),
            'timing': forms.Select(attrs={'class': 'input-field'}),
            'rank': forms.Select(attrs={'class': 'input-field'}),
            'memo': forms.Textarea(attrs={'class': 'input-field'}),
        }

