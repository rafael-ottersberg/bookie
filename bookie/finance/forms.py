from django import forms

from .models import Expense, Income


class expense_form(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'name',
            'amount',
            'category',
            'date',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class income_form(forms.ModelForm):
    class Meta:
        model = Income
        fields = [
            'name',
            'amount',
            'category',
            'date',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }