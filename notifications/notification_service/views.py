from rest_framework import viewsets
from .serializers import ClientSerializer, MailingSerializer, MessageSerializer
from .models import Client, Mailing, Message
from rest_framework.decorators import action
from rest_framework.response import Response
import django.core.exceptions as ex
from django.http import HttpResponseNotFound


class ClientViewSet(viewsets.ModelViewSet):
    """
    This view set deals with a client model
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MailingViewSet(viewsets.ModelViewSet):
    """
    This view set deals with a mailing model
    """
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """
        Shows data for a specific mailing
        """
        try:
            query = Message.objects.filter(mailing_id=pk).all()
            serializer = MessageSerializer(query, many=True)
            return Response(serializer.data)
        except ex.ObjectDoesNotExist:
            return HttpResponseNotFound("There are no messages in this mailing")

    @action(detail=False, methods=['get'])
    def all_stats(self, request):
        """
        Shows data for all mailings
        """
        total_number = Mailing.objects.count()
        mailing = Mailing.objects.values('id')
        content = {'Mailings total': total_number,
                   'The number of messages': ''}
        total_res = {}

        for row in mailing:
            total = {'Messages': 0, 'Sent': 0, 'Not sent': 0}
            messages = Message.objects.filter(mailing_id=row['id']).all()
            sent = messages.filter(status=True).count()
            not_sent = messages.filter(status=False).count()
            total['Messages'] = len(messages)
            total['Sent'] = sent
            total['Not sent'] = not_sent
            total_res[row['id']] = total

        content['The number of messages sent'] = total_res
        return Response(content)
