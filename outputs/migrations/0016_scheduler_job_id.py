# Generated by Django 2.1.10 on 2019-08-21 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outputs', '0015_scheduler_executions'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduler',
            name='job_id',
            field=models.CharField(blank=True, max_length=36),
        ),
    ]