# Generated by Django 2.1.2 on 2019-02-22 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whoismrsaemir', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domains',
            name='url_core',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
