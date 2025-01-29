from django import forms
from .models import Expense, Income
from .models import ExpenseCategoryLimit

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_type', 'amount', 'location', 'date', 'description']  # Fields to display in the form
        widgets = {
            'expense_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['source', 'amount', 'date']  # Fields to display in the form
        widgets = {
            'source': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class ExpenseLimitForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategoryLimit
        fields = ['food_limit', 'transport_limit', 'utility_limit', 'entertainment_limit', 'others_limit']
        widgets = {
            'food_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'transport_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'utility_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'entertainment_limit': forms.NumberInput(attrs={'class': 'form-control'}),
            'others_limit': forms.NumberInput(attrs={'class': 'form-control'}),
        }