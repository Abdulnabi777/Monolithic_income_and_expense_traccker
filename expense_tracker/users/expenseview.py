from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ExpenseForm
from .models import Expense, Income
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ExpenseLimitForm
from .models import ExpenseCategoryLimit, Expense
from django.db import models

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Assign the logged-in user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('home')  # Redirect to the home page (or another page of your choice)
    else:
        form = ExpenseForm()
    
    return render(request, 'add_expense.html', {'form': form})

def set_limits(request):
    # Retrieve or create the user's expense limits
    try:
        category_limits = ExpenseCategoryLimit.objects.get(user=request.user)
    except ExpenseCategoryLimit.DoesNotExist:
        category_limits = ExpenseCategoryLimit(user=request.user)
        category_limits.save()  # Save the newly created instance

    # Handle form submission
    if request.method == 'POST':
        form = ExpenseLimitForm(request.POST, instance=category_limits)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense limits updated successfully!")
            return redirect('set_limits')
    else:
        form = ExpenseLimitForm(instance=category_limits)

    # Check if expenses exceed the limits
    category_expense_limits = {}
    for expense_type, _ in Expense.EXPENSE_TYPES:  # Accessing the EXPENSE_TYPES tuple
        total_expenses = Expense.objects.filter(user=request.user, expense_type=expense_type).aggregate(total=models.Sum('amount'))['total'] or 0
        limit = getattr(category_limits, f"{expense_type}_limit", 0)
        category_expense_limits[expense_type] = {
            'total': total_expenses,
            'limit': limit,
            'exceeded': total_expenses > limit,
        }

    return render(request, 'set_limits.html', {
        'form': form,
        'category_expense_limits': category_expense_limits,
    })

@login_required
def view_expenses(request):
    """View all expenses for the logged-in user and allow editing and deleting."""
    # Fetch the expenses for the logged-in user
    expenses = Expense.objects.filter(user=request.user)
    total_expenses = sum(expense.amount for expense in expenses)  # Calculate total expenses

    # Fetch total income for the logged-in user
    incomes = Income.objects.filter(user=request.user)
    total_income = sum(income.amount for income in incomes)

    # Calculate remaining balance
    remaining_balance = total_income - total_expenses

    # Retrieve category expense limits
    try:
        category_limits = ExpenseCategoryLimit.objects.get(user=request.user)
    except ExpenseCategoryLimit.DoesNotExist:
        category_limits = ExpenseCategoryLimit(user=request.user)
        category_limits.save()  # Create a default limits object if none exists

    # Check if expenses exceed the limits
    category_expense_limits = {}
    for expense_type, _ in Expense.EXPENSE_TYPES:  # Accessing the EXPENSE_TYPES tuple
        total_expenses_by_category = (
            Expense.objects.filter(user=request.user, expense_type=expense_type)
            .aggregate(total=models.Sum('amount'))['total']
            or 0
        )
        limit = getattr(category_limits, f"{expense_type}_limit", 0)
        category_expense_limits[expense_type] = {
            'total': total_expenses_by_category,
            'limit': limit,
            'exceeded': total_expenses_by_category > limit,
        }

    # Pass data to the template
    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'total_income': total_income,
        'remaining_balance': remaining_balance,
        'expenses_exceed_income': total_expenses > total_income,  # Boolean for income alert
        'category_expense_limits': category_expense_limits,  # Add limits to context
    }

    return render(request, 'view_expenses.html', context)

@login_required
def edit_expense(request, expense_id):
    """Edit an existing expense."""
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('view_expenses')
    else:
        form = ExpenseForm(instance=expense)
    
    return render(request, 'edit_expense.html', {'form': form})

@login_required
def delete_expense(request, expense_id):
    """Delete an expense."""
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    expense.delete()
    messages.success(request, 'Expense deleted successfully!')
    return redirect('view_expenses')
