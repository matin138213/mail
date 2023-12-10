from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from mailes.api.permissions import IsAdminSuperUser
from mailes.api.serializers import MailSerializer, MessageSerializer
from mailes.models import Mail, Messages


# Create your views here.


class MailViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAdminSuperUser]
    serializer_class = MailSerializer

    @action(methods=['post'], detail=True, serializer_class=MessageSerializer, permission_classes=[IsAuthenticated])
    def post_massages(self, request, pk):
        try:
            mail = self.get_object()
        except Mail.DoesNotExist:
            return Response({"error": "Mail not found."}, status=404)
        user = self.request.user
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_obj = Messages.objects.create(mail=mail, user=user)

        return Response({'message': f'The massage for mail send {pk}.'})

    def get_queryset(self):
        current_user = self.request.user
        return Mail.objects.filter(owner=current_user) | Mail.objects.filter(
            user=current_user) | Mail.objects.filter(massage_mail__user=current_user)


class MessageViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [IsAdminSuperUser]
    serializer_class = MessageSerializer

    def get_queryset(self):
        current_user = self.request.user

        user_mails = Mail.objects.filter(owner=current_user) | Mail.objects.filter(user=current_user)

        return Messages.objects.filter(mail__in=user_mails)
