from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_alter_about_options_alter_appealcontact_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appealcontact',
            name='subject',
            field=models.CharField(
                blank=True,
                max_length=250,
                null=True,
                verbose_name='Mövzu',
            ),
        ),
    ]
