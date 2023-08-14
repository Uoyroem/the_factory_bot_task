from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


from . import serializers


class UserReadOnlyViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.UserRetrieveSerializer
    queryset = User.objects.all()

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=serializers.UserRegisterSerializer,
    )
    def register(self, request: Request) -> Response:
        serializer = serializers.UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(**serializer.validated_data)
        serializer.validated_data.pop("password")
        return Response(serializer.validated_data)

    @action(
        methods=["POST"], detail=False, serializer_class=serializers.UserLoginSerializer
    )
    def login(self, request: Request) -> Response:
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(
                {"message": "The username or password is not correct."},
                status.HTTP_401_UNAUTHORIZED,
            )
        login(request, user)
        return Response(
            {
                "username": username,
            }
        )
