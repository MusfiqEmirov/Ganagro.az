from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0016_faq'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='is_faq_page_background_image',
            field=models.BooleanField(
                default=False,
                verbose_name='FAQ səhifəsi fon şəkli',
            ),
        ),
    ]
