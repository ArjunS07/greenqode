# Generated by Django 3.2.7 on 2022-03-12 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_communityitem_hasimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityitem',
            name='hasImage',
            field=models.BooleanField(default=False),
        ),
    ]
