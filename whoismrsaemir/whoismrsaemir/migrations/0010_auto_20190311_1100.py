# Generated by Django 2.1.2 on 2019-03-11 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whoismrsaemir', '0009_auto_20190311_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whoisqueue',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]