from django.urls import path
from .userviews import signup_page, login_page, home_page, logout_page, home1_page, report_view
from .apiuserviews import SignupAPI, LoginAPI, LogoutAPI, UserHomeRedirectAPI
from .expenseview import add_expense, view_expenses, edit_expense, delete_expense, set_limits
from .income import add_income, view_incomes, edit_income, delete_income
from .apiexpenseview import AddExpenseAPI, ViewExpensesAPI, EditExpenseAPI, DeleteExpenseAPI, ViewExpenseLimitsAPI, EditExpenseLimitsAPI, CheckExpensesAgainstLimitsAPI
from .adminviews import  manage_users, edit_user, delete_user, user_expenses_graph, user_report
from .apiadminviews import ManageUsersAPI, EditUserAPI, DeleteUserAPI
from .apiincomeviews import AddIncomeAPI, ViewIncomesAPI, EditIncomeAPI, DeleteIncomeAPI
urlpatterns = [
    # API user view
    path('api/signup/', SignupAPI.as_view(), name='api_signup'),
    path('api/login/', LoginAPI.as_view(), name='api_login'),
    path('api/logout/', LogoutAPI.as_view(), name='api_logout'),
    path('api/add_expense/', AddExpenseAPI.as_view(), name='api_add_expense'),
    path('api/redirect_home/', UserHomeRedirectAPI.as_view(), name='api_redirect_home'),
    
    # API user Expenses
    path('api/view_expenses/', ViewExpensesAPI.as_view(), name='api_view_expenses'),
    path('api/edit_expense/<int:expense_id>/', EditExpenseAPI.as_view(), name='api_edit_expense'),
    path('api/delete_expense/<int:expense_id>/', DeleteExpenseAPI.as_view(), name='api_delete_expense'),
    path('api/view_expense_limits/', ViewExpenseLimitsAPI.as_view(), name='api_view_expense_limits'),
    path('api/edit_expense_limits/', EditExpenseLimitsAPI.as_view(), name='api_edit_expense_limits'),
    path('api/check_expenses_against_limits/', CheckExpensesAgainstLimitsAPI.as_view(), name='api_check_expenses_against_limits'),

    # Income management URLs
    path('add-income/', add_income, name='add_income'),
    path('view-incomes/', view_incomes, name='view_incomes'),
    path('edit-income/<int:income_id>/', edit_income, name='edit_income'),
    path('delete-income/<int:income_id>/', delete_income, name='delete_income'),

     #API Income management URLs
    path('api/add-income/', AddIncomeAPI.as_view(), name='api_add_income'),
    path('api/view-incomes/', ViewIncomesAPI.as_view(), name='api_view_incomes'),
    path('api/edit-income/<int:income_id>/', EditIncomeAPI.as_view(), name='api_edit_income'),
    path('api/delete-income/<int:income_id>/', DeleteIncomeAPI.as_view(), name='api_delete_income'),

    # Web user view
    path('signup/', signup_page, name='signup'),
    path('login/', login_page, name='login'),
    path('home1/', home1_page, name='home1'),  # Admin homepage
    path('home/', home_page, name='home'),
    path('report/', report_view, name='report'),
    path('logout/', logout_page, name='logout'),

    # Web user expense
    path('view-expenses/', view_expenses, name='view_expenses'),
    path('add_expense/', add_expense, name='add_expense'),
    path('edit_expense/<int:expense_id>/', edit_expense, name='edit_expense'),
    path('delete_expense/<int:expense_id>/', delete_expense, name='delete_expense'),
    path('set_limits/', set_limits, name='set_limits'),

    #web admin view
    path('manage-users/', manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('user_report/', user_report, name='user_report'),
    path('user_report/<int:user_id>/', user_expenses_graph, name='user_expenses_graph'),
        
    # API for Admin view
    path('api/manage-users/', ManageUsersAPI.as_view(), name='api_manage_users'),
    path('api/edit-user/<int:user_id>/', EditUserAPI.as_view(), name='api_edit_user'),
    path('api/delete-user/<int:user_id>/', DeleteUserAPI.as_view(), name='api_delete_user'),
]
