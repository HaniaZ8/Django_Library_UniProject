# Generated by Django 4.2.5 on 2023-11-12 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_record_author_record_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='surname',
            field=models.CharField(default='None', max_length=100),
        ),
    ]
