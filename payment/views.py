from django.utils import timezone
from datetime import timedelta

from django.db.models import Sum
from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from payment.models import Balance, Transaction
from payment.serializers import (
    BalanceSerializer,
    TransactionSerializer,
    TransactionSummarySerializer
)


class BalanceViewSet(viewsets.ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().select_related("user")
    serializer_class = TransactionSerializer

    def get_serializer_class(self):
        if self.action == "summary":
            return TransactionSummarySerializer
        return self.serializer_class

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Transaction.objects.filter(
                hash=serializer.validated_data["hash"]
        ).exists():
            return Response(
                {"error": "Transaction with this hash already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_transaction = serializer.save()

        balance, created = Balance.objects.get_or_create(
            user=new_transaction.user
        )
        balance.amount += new_transaction.amount
        balance.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        methods=["GET"],
        parameters=[
            OpenApiParameter(
                name="days",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Number of days to look "
                            "back from today for transactions",
                default=7,
            ),
        ],
        description="Retrieve a summary of transactions in the "
                    "specified number of days (ex. ?days=1)."
    )
    @action(detail=False, methods=["GET"], url_path="summary")
    def recent_transactions(self, request):
        days = int(request.query_params.get("days", "7"))
        start_date = timezone.now() - timedelta(days=days)
        transactions = self.queryset.filter(date__gte=start_date)
        total_amount = transactions.aggregate(
            total=Sum("amount")
        )["total"] or 0

        summary_data = {
            "transactions_count": transactions.count(),
            "total_amount": total_amount,
        }

        return Response(summary_data, status=status.HTTP_200_OK)
