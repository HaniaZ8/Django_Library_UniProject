# Generated by Django 4.2.5 on 2024-01-12 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_alter_borrow_borrow_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
    ]
