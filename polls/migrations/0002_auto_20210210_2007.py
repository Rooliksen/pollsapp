# Generated by Django 3.1.6 on 2021-02-10 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
    ]
