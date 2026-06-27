from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_alter_appealcontact_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='value_one',
            field=models.CharField(
                help_text='Məsələn: 25 və ya 90+. Rəqəmdən sonra +, % və s. əlavə edə bilərsiniz.',
                max_length=32,
                verbose_name='1-ci kart — böyük rəqəm',
            ),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='value_two',
            field=models.CharField(
                help_text='Məsələn: 150 və ya 90+. Rəqəmdən sonra +, % və s. əlavə edə bilərsiniz.',
                max_length=32,
                verbose_name='2-ci kart — böyük rəqəm',
            ),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='value_three',
            field=models.CharField(
                help_text='Məsələn: 500 və ya 90+. Rəqəmdən sonra +, % və s. əlavə edə bilərsiniz.',
                max_length=32,
                verbose_name='3-cü kart — böyük rəqəm',
            ),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='value_four',
            field=models.CharField(
                help_text='Məsələn: 1000 və ya 90+. Rəqəmdən sonra +, % və s. əlavə edə bilərsiniz.',
                max_length=32,
                verbose_name='4-cü kart — böyük rəqəm',
            ),
        ),
    ]
