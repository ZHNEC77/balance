from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import UserBalance, BalanceTransaction
from .serializers import (
    BalanceSerializer,
    DepositSerializer,
    TransferSerializer,
    TransactionSerializer
)

User = get_user_model()


class BalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        balance = get_object_or_404(UserBalance, user=request.user)
        serializer = BalanceSerializer(balance)
        return Response(serializer.data)


class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=DepositSerializer,
        responses={
            200: openapi.Response('Успешное пополнение', BalanceSerializer),
            400: openapi.Response('Ошибка валидации'),
            401: openapi.Response('Не авторизован')
        },
        operation_description="Пополнение баланса пользователя"
    )
    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']

        with transaction.atomic():
            balance = UserBalance.objects.select_for_update().get(user=request.user)
            balance.amount += amount
            balance.save()

            BalanceTransaction.objects.create(
                user=request.user,
                amount=amount,
                transaction_type='deposit'
            )

        return Response(
            {'status': 'success', 'balance': balance.amount / 100},
            status=status.HTTP_200_OK
        )


class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=TransferSerializer,
        responses={
            200: openapi.Response('Успешный перевод', examples={
                'application/json': {
                    "status": "success",
                    "sender_balance": 100.0,
                    "recipient_balance": 50.0
                }
            }),
            400: openapi.Response('Ошибка', examples={
                'application/json': {
                    "error": "Недостаточно средств"
                }
            })
        },
        operation_description="Перевод средств другому пользователю"
    )
    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        recipient_id = serializer.validated_data['user_id']

        if request.user.id == recipient_id:
            return Response(
                {'error': 'Нельзя переводить самому себе'},
                status=status.HTTP_400_BAD_REQUEST
            )

        recipient = get_object_or_404(User, id=recipient_id)

        with transaction.atomic():
            sender_balance = UserBalance.objects.select_for_update().get(user=request.user)
            recipient_balance = UserBalance.objects.select_for_update().get(user=recipient)

            if sender_balance.amount < amount:
                return Response(
                    {'error': 'Недостаточно средств'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            sender_balance.amount -= amount
            sender_balance.save()

            recipient_balance.amount += amount
            recipient_balance.save()

            BalanceTransaction.objects.create(
                user=request.user,
                amount=-amount,
                transaction_type='transfer_out',
                related_user=recipient
            )

            BalanceTransaction.objects.create(
                user=recipient,
                amount=amount,
                transaction_type='transfer_in',
                related_user=request.user
            )

        return Response({
            'status': 'success',
            'sender_balance': sender_balance.amount / 100,
            'recipient_balance': recipient_balance.amount / 100
        })


class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = BalanceTransaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
