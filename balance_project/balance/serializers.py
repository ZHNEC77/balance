from rest_framework import serializers
from .models import UserBalance, BalanceTransaction


class BalanceSerializer(serializers.ModelSerializer):
    amount_rub = serializers.SerializerMethodField()

    class Meta:
        model = UserBalance
        fields = ['amount', 'amount_rub']
        read_only_fields = ['amount', 'amount_rub']

    def get_amount_rub(self, obj):
        return obj.amount / 100  # Конвертация копеек в рубли


class DepositSerializer(serializers.Serializer):
    amount = serializers.IntegerField(
        min_value=1,
        help_text="Сумма в копейках"
    )


class TransferSerializer(serializers.Serializer):
    amount = serializers.IntegerField(
        min_value=1,
        help_text="Сумма в копейках"
    )
    user_id = serializers.IntegerField(min_value=1)


class TransactionSerializer(serializers.ModelSerializer):
    amount_rub = serializers.SerializerMethodField()

    class Meta:
        model = BalanceTransaction
        fields = [
            'amount',
            'amount_rub',
            'transaction_type',
            'created_at',
            'related_user'
        ]

    def get_amount_rub(self, obj):
        return obj.amount / 100  # Конвертация копеек в рубли
