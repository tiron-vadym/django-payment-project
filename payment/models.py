from django.db import models

from client.models import User


class Balance(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="balance"
    )
    amount = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    hash = models.TextField(max_length=64, unique=True)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} on {self.date}"
