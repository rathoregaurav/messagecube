from django.db import models

from helper.models import DateModel


class MessageData(DateModel):
    message = models.TextField(db_index=True)
    truth = models.CharField(max_length=20)
    cube = models.CharField(max_length=20)
    google = models.CharField(max_length=255)
    google_spam = models.FloatField()
    google_not_spam = models.FloatField()
    ibm = models.CharField(max_length=255)
    ibm_spam = models.FloatField()
    ibm_not_spam = models.FloatField()

    class Meta:
        db_table = 'message_data'
