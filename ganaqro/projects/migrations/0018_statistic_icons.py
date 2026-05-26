from django.db import migrations, models


ICON_CHOICES = [
    ('bi-people', 'İnsanlar'),
    ('bi-person-check', 'Müştəri'),
    ('bi-person-workspace', 'İşçi'),
    ('bi-building', 'Bina / Ofis'),
    ('bi-globe', 'Dünya'),
    ('bi-geo-alt', 'Məkan'),
    ('bi-truck', 'Nəqliyyat'),
    ('bi-box-seam', 'Məhsul'),
    ('bi-basket', 'Səbət'),
    ('bi-flower1', 'Bitki'),
    ('bi-tree', 'Ağac'),
    ('bi-droplet', 'Su'),
    ('bi-sun', 'Günəş'),
    ('bi-award', 'Mükafat'),
    ('bi-trophy', 'Kubok'),
    ('bi-star', 'Ulduz'),
    ('bi-graph-up', 'Artım'),
    ('bi-bar-chart', 'Qrafik'),
    ('bi-pie-chart', 'Dairəvi qrafik'),
    ('bi-calendar-check', 'Təqvim'),
    ('bi-clock-history', 'Təcrübə'),
    ('bi-shop', 'Mağaza'),
    ('bi-briefcase', 'Biznes'),
]


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_media_faq_page_background_image'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='statistic',
                    name='icon_one',
                    field=models.CharField(
                        blank=True,
                        choices=ICON_CHOICES,
                        default=None,
                        help_text='İstəsəniz boş buraxa bilərsiniz.',
                        max_length=64,
                        null=True,
                        verbose_name='1-ci kart — ikon',
                    ),
                ),
                migrations.AddField(
                    model_name='statistic',
                    name='icon_two',
                    field=models.CharField(
                        blank=True,
                        choices=ICON_CHOICES,
                        default=None,
                        help_text='İstəsəniz boş buraxa bilərsiniz.',
                        max_length=64,
                        null=True,
                        verbose_name='2-ci kart — ikon',
                    ),
                ),
                migrations.AddField(
                    model_name='statistic',
                    name='icon_three',
                    field=models.CharField(
                        blank=True,
                        choices=ICON_CHOICES,
                        default=None,
                        help_text='İstəsəniz boş buraxa bilərsiniz.',
                        max_length=64,
                        null=True,
                        verbose_name='3-cü kart — ikon',
                    ),
                ),
                migrations.AddField(
                    model_name='statistic',
                    name='icon_four',
                    field=models.CharField(
                        blank=True,
                        choices=ICON_CHOICES,
                        default=None,
                        help_text='İstəsəniz boş buraxa bilərsiniz.',
                        max_length=64,
                        null=True,
                        verbose_name='4-cü kart — ikon',
                    ),
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql=(
                        "ALTER TABLE projects_statistic "
                        "ADD COLUMN IF NOT EXISTS icon_one varchar(64) NULL;"
                    ),
                    reverse_sql=(
                        "ALTER TABLE projects_statistic "
                        "DROP COLUMN IF EXISTS icon_one;"
                    ),
                ),
                migrations.RunSQL(
                    sql=(
                        "ALTER TABLE projects_statistic "
                        "ADD COLUMN IF NOT EXISTS icon_two varchar(64) NULL;"
                    ),
                    reverse_sql=(
                        "ALTER TABLE projects_statistic "
                        "DROP COLUMN IF EXISTS icon_two;"
                    ),
                ),
                migrations.RunSQL(
                    sql=(
                        "ALTER TABLE projects_statistic "
                        "ADD COLUMN IF NOT EXISTS icon_three varchar(64) NULL;"
                    ),
                    reverse_sql=(
                        "ALTER TABLE projects_statistic "
                        "DROP COLUMN IF EXISTS icon_three;"
                    ),
                ),
                migrations.RunSQL(
                    sql=(
                        "ALTER TABLE projects_statistic "
                        "ADD COLUMN IF NOT EXISTS icon_four varchar(64) NULL;"
                    ),
                    reverse_sql=(
                        "ALTER TABLE projects_statistic "
                        "DROP COLUMN IF EXISTS icon_four;"
                    ),
                ),
            ],
        ),
    ]
