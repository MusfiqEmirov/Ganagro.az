from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_about_video_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Ad'),
        ),
        migrations.AddField(
            model_name='media',
            name='short_description',
            field=models.TextField(blank=True, null=True, verbose_name='Qısa məlumat'),
        ),
    ]
