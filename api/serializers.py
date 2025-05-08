from rest_framework import serializers
from .models import Transaction, Category

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'amount', 'category', 'date', 'description']

    def validate(self, data):
        # Optionally validate here (e.g., check that the user exists, etc.)
        return data

class CategorySerializer(serializers.ModelSerializer):
    transaction_type_name = serializers.CharField(source='transaction_type.name')
    transaction_type_id = serializers.IntegerField(source='transaction_type.id')

    class Meta:
        model = Category
        fields = ['id', 'name', 'transaction_type_id', 'transaction_type_name']
