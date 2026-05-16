# Generated manually for multilingual Media captions (Haqqımızda gallery).

from django.db import migrations, models


def copy_legacy_to_az(apps, schema_editor):
    Media = apps.get_model('projects', 'Media')
    for row in Media.objects.iterator():
        legacy_name = getattr(row, 'name', None)
        legacy_desc = getattr(row, 'short_description', None)
        if legacy_name or legacy_desc:
            row.name_az = legacy_name or ''
            row.short_description_az = legacy_desc or ''
            row.save(update_fields=('name_az', 'short_description_az'))


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_contact_map_embed_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='name_az',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Ad (AZ)'),
        ),
        migrations.AddField(
            model_name='media',
            name='name_en',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Ad (EN)'),
        ),
        migrations.AddField(
            model_name='media',
            name='name_ru',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Ad (RU)'),
        ),
        migrations.AddField(
            model_name='media',
            name='short_description_az',
            field=models.TextField(blank=True, null=True, verbose_name='Qısa məlumat (AZ)'),
        ),
        migrations.AddField(
            model_name='media',
            name='short_description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Qısa məlumat (EN)'),
        ),
        migrations.AddField(
            model_name='media',
            name='short_description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Qısa məlumat (RU)'),
        ),
        migrations.RunPython(copy_legacy_to_az, migrations.RunPython.noop),
        migrations.RemoveField(model_name='media', name='name'),
        migrations.RemoveField(model_name='media', name='short_description'),
    ]
