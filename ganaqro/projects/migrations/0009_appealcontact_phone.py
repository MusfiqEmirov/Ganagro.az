from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_motto_text_en_alter_motto_text_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appealcontact',
            name='phone',
            field=models.CharField(
                blank=True,
                default='',
                max_length=40,
                verbose_name='Mobil nömrə',
            ),
        ),
    ]
