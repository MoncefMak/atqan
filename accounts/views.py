from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User
from accounts.permissions import CreateUserPermission, DeleteUserPermission, UpdateUserPermission, \
    GetUserPermission
from accounts.serializers import UserSerializer, LogInSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.filter(groups__name='Client').all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [CreateUserPermission]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [UpdateUserPermission]
        elif self.action == 'destroy':
            permission_classes = [DeleteUserPermission]
        elif self.action == 'retrieve':
            permission_classes = [GetUserPermission]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.is_authenticated:
            user = serializer.save(is_active=True, created_by=self.request.user, updated_by=self.request.user)
        else:
            user = serializer.save()
        client_group = Group.objects.get(name='Client')
        user.groups.add(client_group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data)


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer
