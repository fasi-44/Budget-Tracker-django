from django.db import models
from django.contrib.auth.models import User

class TransactionType(models.Model):
    name = models.CharField(max_length=20, choices=[('Income', 'Income'), ('Expense', 'Expense')])

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, db_column='category_name')
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.transaction_type.name} - {self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.month} - {self.amount}"
