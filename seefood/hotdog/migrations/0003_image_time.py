# Generated by Django 3.1.4 on 2020-12-26 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotdog', '0002_auto_20201226_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
