# Generated by Django 4.2.13 on 2024-05-25 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lyrics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lyric',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
