from django.contrib import admin

from payment.models import Balance, Transaction


admin.site.register(Balance)
admin.site.register(Transaction)
