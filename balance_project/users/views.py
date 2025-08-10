from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import PermissionDenied
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.kwargs.get('pk') == 'me':
            return self.request.user
        obj = super().get_object()
        if obj != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied(
                "Вы можете просматривать только свой профиль")
        return obj


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        if user:
            # Создаем токен для нового пользователя
            Token.objects.create(user=user)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        operation_description="Аутентификация пользователя",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Успешная аутентификация",
                examples={
                    "application/json": {
                        "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
                        "user_id": 1,
                        "username": "admin"
                    }
                }
            ),
            400: openapi.Response(
                description="Неверные данные",
                examples={
                    "application/json": {
                        "username": ["Это поле обязательно."],
                        "password": ["Это поле обязательно."]
                    }
                }
            )
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username
                })
            return Response(
                {'error': 'Invalid Credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post', 'options']

    def post(self, request):
        try:
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
