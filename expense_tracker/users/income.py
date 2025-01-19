from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import IncomeForm
from .models import Income

@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user  # Assign the logged-in user
            income.save()
            messages.success(request, 'Income added successfully!')
    else:
        form = IncomeForm()

    return render(request, 'add_income.html', {'form': form})

@login_required
def view_incomes(request):
    incomes = Income.objects.filter(user=request.user)  # Get incomes for the logged-in user
    return render(request, 'view_incomes.html', {'incomes': incomes})

@login_required
def edit_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            messages.success(request, 'Income updated successfully!')
            return redirect('view_incomes')
    else:
        form = IncomeForm(instance=income)

    return render(request, 'edit_income.html', {'form': form})

@login_required
def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id, user=request.user)
    income.delete()
    messages.success(request, 'Income deleted successfully!')
    return redirect('view_incomes')
