# Generated by Django 2.0.13 on 2021-03-02 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_nickname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='nickname',
        ),
    ]
