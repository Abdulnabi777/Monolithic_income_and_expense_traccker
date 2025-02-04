from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Expense
from django.contrib.admin.views.decorators import staff_member_required
import plotly.graph_objects as go
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Expense, Income
from django.db.models import Sum

# Web: Signup Page
def signup_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Get the selected role

        if username and email and password and role:
            user = User.objects.create_user(username=username, email=email, password=password)
            
            # Assign the role (admin or user) to the user
            if role == 'admin':
                user.is_staff = True  # This gives the user admin permissions
            user.save()

            return redirect('login')
    return render(request, 'signup.html')

# Web: Login Page
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Get the user by email
            user = User.objects.get(email=email)
            # Authenticate using the username field (email is not used directly)
            user = authenticate(username=user.username, password=password)
            if user:
                login(request, user)
                # Redirect admin users to home1 and regular users to home
                if user.is_staff:
                    return redirect('home1')  # Redirect to admin homepage
                return redirect('home')  # Redirect to regular user homepage
            else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('login') 
 
def password_reset_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)  # Reset the password
            user.save()
            return redirect('login')  # Redirect to login after reset
        except User.DoesNotExist:
            return render(request, 'password_reset.html', {'error': 'User does not exist'})

    return render(request, 'password_reset.html')

@staff_member_required  # Ensures only admin users can access this view
def home1_page(request):
    return render(request, 'home1.html') 

@login_required
def report_view(request):
    # Fetch the user's income and expenses
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    # Summarize income and expenses by month
    income_data = incomes.values('date__month').annotate(total_amount=Sum('amount')).order_by('date__month')
    expense_data = expenses.values('date__month').annotate(total_amount=Sum('amount')).order_by('date__month')

    # Prepare data for the graph
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    income_by_month = [0] * 12
    expense_by_month = [0] * 12

    for income in income_data:
        income_by_month[income['date__month'] - 1] = income['total_amount']

    for expense in expense_data:
        expense_by_month[expense['date__month'] - 1] = expense['total_amount']

    # Get the type of chart (bar graph or line graph) from the GET parameters
    chart_type = request.GET.get('chart_type', 'bar')  # Default to bar graph

    if chart_type == 'line':
        # Create a line chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=income_by_month, mode='lines+markers', name='Income', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=months, y=expense_by_month, mode='lines+markers', name='Expense', line=dict(color='red')))
        fig.update_layout(
            title="Income vs Expenses (Line Chart)",
            xaxis_title="Months",
            yaxis_title="Amount",
        )
    else:
        # Create a bar graph
        fig = go.Figure()
        fig.add_trace(go.Bar(x=months, y=income_by_month, name='Income', marker_color='green'))
        fig.add_trace(go.Bar(x=months, y=expense_by_month, name='Expense', marker_color='red'))
        fig.update_layout(
            title="Income vs Expenses",
            xaxis_title="Months",
            yaxis_title="Amount",
            barmode='group',
        )

    # Convert the graph to HTML
    graph_div = fig.to_html(full_html=False)

    return render(request, 'report.html', {'graph_div': graph_div, 'chart_type': chart_type})


# Web: Home Page
@login_required
def home_page(request):
    # Fetch the expenses for the logged-in user
    expenses = Expense.objects.filter(user=request.user)

    # Pass the expenses to the template
    return render(request, 'home.html', {'expenses': expenses})

 