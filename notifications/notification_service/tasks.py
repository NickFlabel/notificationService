import datetime
from celery import current_app
import os
from .models import Message, Client, Mailing
import pytz
import requests
from django.core.mail import send_mail
from celery.schedules import crontab

app = current_app._get_current_object()
URL = os.environ['FETCH_URL']
JWT = os.environ['JWT']
RECEIVER_EMAIL = os.environ['RECEIVER_EMAIL']

@app.task
def send_stats():
    """
    Fetches messages data and sends it to a given email (env variable)
    """
    today = datetime.today()

    year = today.year
    month = today.month
    day = today.day
    messages = Message.objects.filter(created_at__year=year, created_at__month=month, created_at__day=day)
    data = ''
    for message in messages:
        data += "Message #" + message.id + '\n' + "Message status:" + message.status + '\n' + "Created:" + message.created_at + "\n\n"
    send_mail("Daily Report", data, "test@django.com", [RECEIVER_EMAIL])


@app.task(bind=True, retry_backoff=True)
def send_message(self, data, client_id, mailing_id, url=URL, token=JWT):
    """
    This task sets up messaging
    """
    mailing = Mailing.objects.get(pk=mailing_id)
    client = Client.objects.get(pk=client_id)
    tz = pytz.timezone(client.timezone)
    now = datetime.datetime.now(tz)

    if mailing.start_datetime <= now <= mailing.end_datetime:
        header = {
            "Authorization": f'Bearer {token}',
            "Content-Type": "application/json"
        }
        try:
            requests.post(
                url=url + str(data['id']),
                headers=header,
                json=data
            )
        except requests.exceptions.RequestException as exc:
            raise self.retry(exc=exc)
        else:
            Message.objects.filter(pk=data['id']).update(status=True)
    else:
        time = 24 - (int(now.time().strftime('%H:%M:%S')[:2]) - int(mailing.start_datetime.strftime('%H:%M:%S')[:2]))

        return self.retry(countdown=60*60*time)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """This function sets up the periodic messaging of the stats
    """
    sender.add_periodic_task(crontab(minute=00, hour=9), send_stats.s(), name="periodic messages")