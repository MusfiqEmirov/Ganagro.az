from django.db import models
from django.core.validators import MaxLengthValidator


class Motto(models.Model):
    text_az = models.TextField(
        validators=[MaxLengthValidator(220)],
        verbose_name='Deviz cümləsi(AZ)'
    )
    text_en = models.TextField(
        validators=[MaxLengthValidator(220)],
        verbose_name='Deviz cümləsi(EN)'
    )
    text_ru = models.TextField(
        validators=[MaxLengthValidator(220)],
        verbose_name='Deviz cümləsi(RU)'
    )

    class Meta:
        verbose_name = 'Deviz'
        verbose_name_plural = 'Deviz'

    def __str__(self):
        return 'Deviz'