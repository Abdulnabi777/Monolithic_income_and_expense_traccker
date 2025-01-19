from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
import plotly.graph_objects as go
from django.db.models import Sum
from .models import Expense, Income
from django.db.models.functions import Coalesce
from django.db import models
from decimal import Decimal

# Admin view to manage users with pagination
@staff_member_required
def manage_users(request):
    # Fetch all users except superuser
    user_list = User.objects.exclude(is_superuser=True)  # Optionally exclude superusers
    paginator = Paginator(user_list, 10)  # Show 10 users per page
    
    page_number = request.GET.get('page')  # Get the current page number
    users = paginator.get_page(page_number)  # Get users for the current page
    
    return render(request, 'manage_users.html', {'users': users})


# View for Editing a User
@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        is_staff = request.POST.get('is_staff') == 'on'
        user.username = username
        user.email = email
        user.is_staff = is_staff
        user.save()
        return redirect('manage_users')
    return render(request, 'edit_user.html', {'user': user})


# View for Deleting a User
@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('manage_users')
    return render(request, 'delete_user.html', {'user': user})

@staff_member_required
def user_report(request):
    # Aggregate total expenses and total income for each non-superuser
    user_expenses_and_income = (
        User.objects
        .exclude(is_superuser=True)  # Explicitly exclude superusers (admins)
        .annotate(
            total_expenses=Coalesce(Sum('expense__amount', output_field=models.DecimalField()), Decimal('0')),  # Use Decimal(0) instead of DecimalField
            total_income=Coalesce(Sum('income__amount', output_field=models.DecimalField()), Decimal('0'))      # Use Decimal(0) instead of DecimalField
        )
    )

    # Calculate total number of non-superuser users
    total_users = User.objects.exclude(is_superuser=True).count()

    # Calculate total expenses (across all users)
    total_expenses = Expense.objects.aggregate(total=Coalesce(Sum('amount', output_field=models.DecimalField()), Decimal('0')))['total']

    # Calculate total income (across all users)
    total_income = Income.objects.aggregate(total=Coalesce(Sum('amount', output_field=models.DecimalField()), Decimal('0')))['total']

    # Pass the data to the template
    context = {
        'user_expenses_and_income': user_expenses_and_income,
        'total_users': total_users,
        'total_expenses': total_expenses,
        'total_income': total_income,
    }

    return render(request, 'user_report.html', context)

@staff_member_required
def user_expenses_graph(request, user_id):
    user = get_object_or_404(User, id=user_id)
    expenses = Expense.objects.filter(user=user).values('date__month').annotate(total_amount=Sum('amount'))

    # Prepare monthly data
    months = [
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    monthly_expenses = [0] * 12
    for expense in expenses:
        monthly_expenses[expense['date__month'] - 1] = expense['total_amount']

    # Create a bar graph
    fig = go.Figure()
    fig.add_trace(go.Bar(x=months, y=monthly_expenses, name='Expenses', marker_color='red'))
    fig.update_layout(
        title=f"Monthly Expenses for {user.username}",
        xaxis_title="Months",
        yaxis_title="Amount",
    )
    graph_div = fig.to_html(full_html=False)

    return render(request, 'user_expenses_graph.html', {'graph_div': graph_div, 'user': user})
