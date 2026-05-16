# Generated manually for Statistic caption fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_alter_media_verbose_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='caption_one_az',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Say 1 — alt yazı (AZ)'),
        ),
        migrations.AddField(
            model_name='statistic',
            name='caption_one_en',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Say 1 — alt yazı (EN)'),
        ),
        migrations.AddField(
            model_name='statistic',
            name='caption_one_ru',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Say 1 — alt yazı (RU)'),
        ),
        migrations.AddField(
            model_name='statistic',
            name='caption_two_az',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Say 2 — alt yazı (AZ)'),
        ),
        migrations.AddField(
            model_name='statistic',
            name='caption_two_en',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Say 2 — alt yazı (EN)'),
        ),
        migrations.AddField(
            model_name='statistic',
            name='caption_two_ru',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Say 2 — alt yazı (RU)'),
        ),
        migrations.AddField(
            model_name='statistic',
            name='caption_three_az',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Say 3 — alt yazı (AZ)'),
        ),
        migrations.AddField(
            model_name='statistic',
            name='caption_three_en',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Say 3 — alt yazı (EN)'),
        ),
        migrations.AddField(
            model_name='statistic',
            name='caption_three_ru',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Say 3 — alt yazı (RU)'),
        ),
        migrations.AddField(
            model_name='statistic',
            name='caption_four_az',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Say 4 — alt yazı (AZ)'),
        ),
        migrations.AddField(
            model_name='statistic',
            name='caption_four_en',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Say 4 — alt yazı (EN)'),
        ),
        migrations.AddField(
            model_name='statistic',
            name='caption_four_ru',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Say 4 — alt yazı (RU)'),
        ),
    ]
