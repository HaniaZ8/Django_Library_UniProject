# Generated by Django 4.2.5 on 2024-01-14 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='death_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
