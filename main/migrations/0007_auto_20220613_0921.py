# Generated by Django 3.2.7 on 2022-06-13 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20220529_0931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='communityitemgroup',
            name='location',
        ),
        migrations.AlterField(
            model_name='communityitemgroupthrough',
            name='alive',
            field=models.IntegerField(default=0),
        ),
    ]
