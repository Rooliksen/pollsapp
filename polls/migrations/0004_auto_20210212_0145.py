# Generated by Django 3.1.6 on 2021-02-11 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20210212_0117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='choice',
        ),
        migrations.AddField(
            model_name='answer',
            name='choice',
            field=models.ManyToManyField(to='polls.Choice'),
        ),
    ]
