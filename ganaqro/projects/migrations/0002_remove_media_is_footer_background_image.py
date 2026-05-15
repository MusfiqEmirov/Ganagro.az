# Generated manually for footer background removal

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='is_footer_background_image',
        ),
    ]
