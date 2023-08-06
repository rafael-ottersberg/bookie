from django import forms

from .models import Expense, Income


class ExpenseForm(forms.ModelForm):
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

class IncomeForm(forms.ModelForm):
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