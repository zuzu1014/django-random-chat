# Generated by Django 2.0.13 on 2021-01-28 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(max_length=30, verbose_name='nickname'),
        ),
    ]
