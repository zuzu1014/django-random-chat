# Generated by Django 2.0.13 on 2021-03-02 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_user_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='tmp', max_length=127),
            preserve_default=False,
        ),
    ]
