from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class UserBalance(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='balance'
    )
    amount = models.BigIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )  # Храним в копейках

    def __str__(self):
        return f"{self.user.username}: {self.amount / 100:.2f} руб."


class BalanceTransaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Пополнение'),
        ('transfer_out', 'Исходящий перевод'),
        ('transfer_in', 'Входящий перевод'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    amount = models.BigIntegerField()
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    related_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_transactions'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_transaction_type_display()}: {self.amount / 100:.2f} руб."
