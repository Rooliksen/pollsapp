# Generated by Django 3.1.6 on 2021-02-13 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20210213_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='choice',
        ),
        migrations.AddField(
            model_name='answer',
            name='cboice_one',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answers_one_choice', to='polls.choice'),
        ),
        migrations.AddField(
            model_name='answer',
            name='choice_many',
            field=models.ManyToManyField(related_name='answers_many_choice', to='polls.Choice'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='choice_text',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='polls.poll'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='polls.question'),
        ),
    ]