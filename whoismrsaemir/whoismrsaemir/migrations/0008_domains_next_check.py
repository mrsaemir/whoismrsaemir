# Generated by Django 2.1.2 on 2019-03-10 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whoismrsaemir', '0007_auto_20190310_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='domains',
            name='next_check',
            field=models.DateField(null=True),
        ),
    ]
