from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, Category, Budget
from django.db.models import Sum, Count, Q
from datetime import datetime
from .serializers import CategorySerializer
from datetime import date
from django.shortcuts import get_object_or_404
from collections import defaultdict
from django.core.paginator import Paginator
from api.serializers import TransactionSerializer

@api_view(['POST'])
def login(request):
    print("inside the login")
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = User.objects.get(email=email)
        user = authenticate(username=user.username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "token": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "username": user.username,
                    "email": user.email,
                    'userId': user.id,
                }
            })
        else:
            return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({"message": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_total_income_or_expense(request):
    user_id = request.GET.get('userId')
    type_id = request.GET.get('transactionTypeId')
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    
    print(f"Received parameters: userId={user_id}, transactionTypeId={type_id}, month={month}, year={year}")
    

    total = Transaction.objects.filter(
        user_id=user_id,
        category__transaction_type_id=type_id,
        date__month=month,
        date__year=year
    ).aggregate(total=Sum('amount'))['total'] or 0

    return Response({'status': 'SUCCESS', 'response': float(total)}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_total_no_of_transactions(request):
    user_id = request.GET.get('userId')
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))

    total = Transaction.objects.filter(
        user_id=user_id,
        date__month=month,
        date__year=year
    ).count()

    return Response({'status': 'SUCCESS', 'response': total}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_total_by_category(request):
    print("isnide the get_total_by_category")
    email = request.GET.get('email')
    category_id = request.GET.get('categoryId')
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    
    print(f"Email: {email}, Category ID: {category_id}, Month: {month}, Year: {year}")
    user = get_object_or_404(User, email=email)

    total = Transaction.objects.filter(
        user=user,
        category_id=category_id,
        date__month=month,
        date__year=year
    ).aggregate(total=Sum('amount'))['total'] or 0

    return Response({'status': 'SUCCESS', 'response': float(total)}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_budget(request):
    user = request.GET.get('userId')
    month = int(request.GET.get('month'))
    year = int(request.GET.get('year'))
    
    budget = Budget.objects.filter(
        user=user,
        month__month=month,
        month__year=year
    ).first()

    return Response({
        'status': 'SUCCESS',
        'response': float(budget.amount) if budget else 0
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_or_update_budget(request):
    user = request.user
    amount = request.data.get('amount')

    today = date.today()
    budget, created = Budget.objects.update_or_create(
        user=user,
        month__month=today.month,
        month__year=today.year,
        defaults={'amount': amount, 'month': today}
    )

    return Response({
        'status': 'SUCCESS',
        'message': 'Budget saved successfully.'
    }, status=status.HTTP_200_OK)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transaction(request):
    user = request.user
    
    # Extract data from request
    category_id = request.data.get('categoryId')
    description = request.data.get('description')
    amount = request.data.get('amount')
    date = request.data.get('date')
    
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response({"status": "FAILURE", "response": "Category not found."}, status=status.HTTP_400_BAD_REQUEST)


    # Creating the transaction
    transaction = Transaction.objects.create(
        user=user,
        amount=amount,
        category=category,
        description=description,
        date=date
    )

    return Response({"status": "SUCCESS", "response": "Transaction added successfully!"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response({'status': 'SUCCESS', 'response': serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transactions_by_user(request):
    email = request.GET.get('email')
    page_number = int(request.GET.get('pageNumber', 0))
    page_size = int(request.GET.get('pageSize', 10))
    transaction_type = request.GET.get('transactionType')  # Optional

    user = User.objects.get(email=email)
    transactions = Transaction.objects.filter(user=user)

    if transaction_type:
        transactions = transactions.filter(category__transaction_type_id=transaction_type)

    transactions = transactions.order_by('-date')

    # Pagination (optional)
    total_records = transactions.count()
    start = page_number * page_size
    end = start + page_size
    paginated_transactions = transactions[start:end]

    # Group transactions by date
    grouped = defaultdict(list)
    for t in paginated_transactions:
        date_str = t.date.strftime('%Y-%m-%d')
        grouped[date_str].append({
            "transactionId": t.id,
            "amount": str(t.amount),
            "categoryId": t.category.id,
            "categoryName": t.category.name,
            "description": t.description,
            "transactionType": t.category.transaction_type_id,
            "date": date_str
        })

    return Response({
        "status": "SUCCESS",
        "response": {
            "data": grouped,
            "totalNoOfPages": (total_records + page_size - 1) // page_size,
            "totalNoOfRecords": total_records
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transaction_by_id(request):
    transaction_id = request.GET.get('id')

    if not transaction_id or not transaction_id.isdigit():
        return Response({
            "status": "FAILURE",
            "response": "Invalid or missing transaction ID."
        }, status=400)

    try:
        transaction = Transaction.objects.select_related('category', 'user').get(id=int(transaction_id))
    except Transaction.DoesNotExist:
        return Response({
            "status": "FAILURE",
            "response": "Transaction not found."
        }, status=404)

    transaction_data = {
        "transactionId": transaction.id,
        "amount": str(transaction.amount),
        "categoryId": transaction.category.id,
        "categoryName": transaction.category.name,
        "description": transaction.description,
        "transactionType": transaction.category.transaction_type_id,
        "date": transaction.date.strftime('%Y-%m-%d'),
        "userEmail": transaction.user.email
    }

    return Response({
        "status": "SUCCESS",
        "response": transaction_data
    })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_transaction(request):
    transaction_id = request.GET.get('transactionId')
    data = request.data

    # Validate required data
    if not transaction_id or not transaction_id.isdigit():
        return Response({"status": "FAILURE", "response": "Invalid or missing transaction ID."}, status=400)

    try:
        transaction = Transaction.objects.get(id=int(transaction_id))
    except Transaction.DoesNotExist:
        return Response({"status": "FAILURE", "response": "Transaction not found for this user."}, status=404)

    # Update transaction fields
    try:
        category_id = data.get('categoryId')
        category = Category.objects.get(id=category_id)

        transaction.category = category
        transaction.description = data.get('description', transaction.description)
        transaction.amount = data.get('amount', transaction.amount)
        transaction.date = data.get('date', transaction.date)
        transaction.save()

        return Response({
            "status": "SUCCESS",
            "response": "Transaction updated successfully."
        })
    except Category.DoesNotExist:
        return Response({"status": "FAILURE", "response": "Invalid category ID."}, status=404)
    except Exception as e:
        return Response({"status": "FAILURE", "response": str(e)}, status=500)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_transaction(request):
    transaction_id = request.GET.get('transactionId')

    if not transaction_id or not transaction_id.isdigit():
        return Response({ "status": "FAILURE", "response": "Invalid or missing transaction ID."}, status=400)

    try:
        transaction = Transaction.objects.get(id=int(transaction_id))
    except Transaction.DoesNotExist:
        return Response({ "status": "FAILURE", "response": "Transaction not found."}, status=404)

    transaction.delete()

    return Response({ "status": "SUCCESS", "response": "Transaction deleted successfully." })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_budget(request):
    user_id = request.data.get('userId')
    amount = request.data.get('amount')
    print(f"Received parameters: userId={user_id}, amount={amount}")
    if not user_id or amount is None:
        return Response({'status': 'FAILED', 'response': 'Missing userId or amount.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'status': 'FAILED', 'response': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    # Use the 1st of the current month to store the date
    today = datetime.today()
    month_start = datetime(today.year, today.month, 1).date()

    # Update if budget exists for this user and month
    budget, created = Budget.objects.update_or_create(
        user=user,
        month=month_start,
        defaults={'amount': amount}
    )

    return Response({
        'status': 'SUCCESS',
        'response': f"{'Created' if created else 'Updated'} budget successfully."
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    name = request.data.get('categoryName')
    transaction_type_id = request.data.get('transactionTypeId')

    if not name or not transaction_type_id:
        return Response({'status': 'FAILED', 'response': 'Missing categoryName or transactionTypeId'},
                        status=status.HTTP_400_BAD_REQUEST)

    Category.objects.create(
        name=name,
        transaction_type_id=transaction_type_id,
    )

    return Response({'status': 'SUCCESS', 'response': 'Category created successfully'},
                    status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_category(request):
    category_id = request.query_params.get('categoryId')
    name = request.data.get('categoryName')
    transaction_type_id = request.data.get('transactionTypeId')

    if not category_id or not name or not transaction_type_id:
        return Response({'status': 'FAILED', 'response': 'Missing required fields'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        category = Category.objects.get(id=category_id)
        category.name = name
        category.transaction_type_id = transaction_type_id
        category.save()

        return Response({'status': 'SUCCESS', 'response': 'Category updated successfully'},
                        status=status.HTTP_200_OK)

    except Category.DoesNotExist:
        return Response({'status': 'FAILED', 'response': 'Category not found'},
                        status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_monthly_summary_by_user(request):
    user = request.user
    email = request.GET.get('email')
    year = datetime.now().year  # default to current year, or make it request.GET.get('year')

    # Filter transactions for the user and year
    transactions = Transaction.objects.filter(user__email=email, date__year=year)

    monthly_summary = []

    for month in range(1, 13):
        month_transactions = transactions.filter(date__month=month)
        income = month_transactions.filter(category__transaction_type__name__iexact='INCOME').aggregate(total=Sum('amount'))['total'] or 0
        expense = month_transactions.filter(category__transaction_type__name__iexact='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0

        monthly_summary.append({
            'month': month,
            'year': year,
            'income': float(income),
            'expense': float(expense)
        })

    return Response({
        'status': 'SUCCESS',
        'response': monthly_summary
    })