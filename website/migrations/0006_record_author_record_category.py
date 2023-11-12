# Generated by Django 4.2.5 on 2023-11-12 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_author_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.author'),
        ),
        migrations.AddField(
            model_name='record',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.category'),
        ),
    ]
