# Generated by Django 4.2.5 on 2023-11-12 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_remove_record_first_name_remove_record_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='borrow_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]