# Generated by Django 3.2.12 on 2022-03-29 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0005_alter_wallet_enabled_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='enabled_at',
            field=models.DateTimeField(default='2022-03-29T01:52:31.801634+00:00'),
        ),
    ]