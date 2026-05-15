from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_about_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='about',
            name='video_poster',
            field=models.ImageField(
                blank=True,
                help_text='Cover frame shown before play (recommended — square image works best).',
                null=True,
                upload_to='images/about/video_posters/',
                verbose_name='Video örtüyü (poster)',
            ),
        ),
    ]
