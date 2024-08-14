from rest_framework import serializers
from payment.models import Balance, Transaction


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ("id", "user", "amount")


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("id", "user", "hash", "amount", "date")


class TransactionSummarySerializer(TransactionSerializer):
    days = serializers.IntegerField()

    class Meta:
        model = Transaction
        fields = ("id", "days")
