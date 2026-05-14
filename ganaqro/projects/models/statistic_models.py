from django.db import models
from django.core.validators import MaxLengthValidator

class Statistic(models.Model):
    value_one = models.PositiveIntegerField(
        verbose_name='Dəyər sayı 1'
    )
    value_two = models.PositiveIntegerField(
        verbose_name='Dəyər sayı 2'
    )
    value_three = models.PositiveIntegerField(
        verbose_name='Dəyər sayı 3'
    )
    value_four = models.PositiveIntegerField(
        verbose_name='Dəyər sayı 4'
    )

    class Meta:
        verbose_name = 'Statistika'
        verbose_name_plural = 'Statistikalar'

    def __str__(self):
        return 'Statistika'

   
    
   
