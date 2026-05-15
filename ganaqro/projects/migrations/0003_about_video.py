import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_remove_media_is_footer_background_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='video',
            field=models.FileField(
                blank=True,
                help_text='Single promotional video for the About page (optional).',
                null=True,
                upload_to='videos/about/',
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=('mp4', 'webm', 'mov', 'ogg', 'mkv'),
                        message='Allowed formats: mp4, webm, mov, ogg, mkv.',
                    )
                ],
                verbose_name='Video',
            ),
        ),
    ]
