from django.db import migrations, models


def set_initial_main_page_blogs(apps, schema_editor):
    Blog = apps.get_model('projects', 'Blog')
    ids = list(
        Blog.objects.order_by('-date', '-created_at').values_list('pk', flat=True)[:6]
    )
    if ids:
        Blog.objects.filter(pk__in=ids).update(on_main_page=True)


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_motto_page_flags'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='on_main_page',
            field=models.BooleanField(
                default=False,
                help_text='Ana səhifədə ən çox 6 bloq göstərilir.',
                verbose_name='Ana səhifədə olsun',
            ),
        ),
        migrations.RunPython(set_initial_main_page_blogs, noop_reverse),
    ]
