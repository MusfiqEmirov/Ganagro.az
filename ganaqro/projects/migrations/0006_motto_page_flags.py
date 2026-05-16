from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_media_name_short_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='motto',
            name='show_on_home_hero',
            field=models.BooleanField(default=True, verbose_name='Ana səhifə karuselində göstər'),
        ),
        migrations.AddField(
            model_name='motto',
            name='is_about_page',
            field=models.BooleanField(default=False, verbose_name='Haqqımızda səhifəsi'),
        ),
        migrations.AddField(
            model_name='motto',
            name='is_contact_page',
            field=models.BooleanField(default=False, verbose_name='Əlaqə səhifəsi'),
        ),
        migrations.AddField(
            model_name='motto',
            name='is_product_page',
            field=models.BooleanField(default=False, verbose_name='Məhsullar (kateqoriya) səhifəsi'),
        ),
        migrations.AddField(
            model_name='motto',
            name='is_blog_page',
            field=models.BooleanField(default=False, verbose_name='Bloq səhifəsi'),
        ),
    ]
