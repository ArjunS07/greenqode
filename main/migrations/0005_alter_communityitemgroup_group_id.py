# Generated by Django 3.2.7 on 2022-05-28 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_rename_itemgroup_communityitemgroupthrough_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityitemgroup',
            name='group_id',
            field=models.CharField(default=None, max_length=108, null=True),
        ),
    ]
