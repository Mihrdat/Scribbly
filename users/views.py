from django.db import transaction
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    TokenSerializer,
)
from .pagination import DefaultLimitOffsetPagination

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultLimitOffsetPagination

    @action(methods=["GET", "PUT", "PATCH"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_current_user
        if request.method == "PUT":
            return self.update(request, *args, **kwargs)
        if request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)

    @transaction.atomic
    @action(methods=["POST"], detail=False)
    def change_password(self, request, *args, **kwargs):
        user = self.get_current_user()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.data["new_password"])
        user.save(update_fields=["password"])

        # Log out user from other systems after changing the password
        Token.objects.get(user=user).delete()

        new_token = Token.objects.create(user=user)
        serializer = TokenSerializer(new_token)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_current_user(self):
        return self.request.user

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            self.queryset = self.queryset.filter(pk=user.pk)
        return super().get_queryset()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = UserCreateSerializer
        if self.action == "change_password":
            self.serializer_class = ChangePasswordSerializer
        if self.action in ["update", "partial_update"]:
            self.serializer_class = UserUpdateSerializer
        return super().get_serializer_class()
