from django.db import models

# Create your models here.
import datetime
class EntryModel(models.Model):
    date = models.DateField(default=datetime.date.today)
    entry = models.CharField(blank=True, max_length=30)
    entry_body = models.CharField(default='detail', max_length=3000)
    amount = models.IntegerField(blank=True)
    owner = models.EmailField(blank=True, max_length=330)
    pre_delete = models.BooleanField(default=False)
    
    # class Meta:
    #     ordering=['tdate']
