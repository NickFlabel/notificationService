from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from .models import Mailing, Client, Message
from .tasks import send_message


@receiver(post_save, sender=Mailing, dispatch_uid="create_message")
def create_message(sender, instance, created, **kwargs):
    if created:
        mailing = Mailing.objects.filter(id=instance.id).first()
        clients = Client.objects.filter(Q(operator_code=mailing.filter_code) |
                                        Q(tag=mailing.filter_tag)).all()

        for client in clients:
            Message.objects.create(
                status=False,
                client_id=client,
                mailing_id=instance
            )
            message = Message.objects.filter(mailing_id=instance.id, client_id=client.id).first()
            data = {
                'id': message.id,
                "phone": client.phone_number,
                "text": mailing.text
            }
            mailing_id = mailing.id
            client_id = client.id

            if instance.is_due:
                send_message.apply_async((data, client_id, mailing_id),
                                         expires=mailing.end_datetime)
            else:
                send_message.apply_async((data, client_id, mailing_id),
                                         eta=mailing.start_datetime, expires=mailing.end_datetime)
