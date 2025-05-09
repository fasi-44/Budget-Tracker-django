from django.urls import path
from .views import (
    login,
    get_total_income_or_expense,
    get_total_no_of_transactions,
    get_total_by_category,
    get_budget,
    create_or_update_budget,
    create_transaction, 
    get_all_categories,
    get_transactions_by_user,
    get_transaction_by_id,
    update_transaction,
    delete_transaction,
    create_budget,update_category,create_category,get_monthly_summary_by_user
)

urlpatterns = [
    path('auth/signin', login),
    path('report/getTotalIncomeOrExpense', get_total_income_or_expense),
    path('report/getTotalNoOfTransactions', get_total_no_of_transactions),
    path('report/getTotalByCategory', get_total_by_category),
    path('budget/get', get_budget),
    path('report/createBudget', create_or_update_budget),
    path('transaction/new', create_transaction),
    path('category/getAll', get_all_categories), 
    path('transaction/getByUser', get_transactions_by_user), 
    path('transaction/getById', get_transaction_by_id), 
    path('transaction/update', update_transaction), 
    path('transaction/delete', delete_transaction), 
    path('budget/create', create_budget),
    path('category/update', update_category),
    path('category/new', create_category),
    path('report/getMonthlySummaryByUser', get_monthly_summary_by_user),
]
