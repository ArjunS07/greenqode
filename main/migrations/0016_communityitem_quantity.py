# Generated by Django 3.2.7 on 2022-04-08 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20220318_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='communityitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
