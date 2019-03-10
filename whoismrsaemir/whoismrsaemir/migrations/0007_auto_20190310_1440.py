# Generated by Django 2.1.2 on 2019-03-10 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whoismrsaemir', '0006_domains_count_down_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhoisQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='whoismrsaemir.Domains')),
            ],
        ),
        migrations.RemoveField(
            model_name='dailydomainchecks',
            name='url_core',
        ),
        migrations.DeleteModel(
            name='DailyDomainChecks',
        ),
    ]