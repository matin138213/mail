from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from mailes.api.permissions import IsAdminSuperUser
from mailes.api.serializers import MailSerializer, MessageSerializer
from mailes.models import Mail, Messages


# Create your views here.


class MailViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAdminSuperUser]
    serializer_class = MailSerializer

    def get_queryset(self):
        return Mail.objects.filter(user=self.request.user)


class MessageViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = [IsAdminSuperUser]
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Messages.objects.filter(user=self.request.user)
