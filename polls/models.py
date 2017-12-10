from django.db import models

# Create your models here.

from datetime import datetime, timedelta
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField('texto de la pregunta', max_length=200)
    pub_date = models.DateTimeField('fecha de publicación')
    
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - timedelta(days=1)
    
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '¿Publicada recientemente?'    

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text