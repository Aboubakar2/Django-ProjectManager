# Generated by Django 5.0.1 on 2024-02-15 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_team_tasks_alter_task_teams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='tasks',
            field=models.ManyToManyField(related_name='tasks_todo', to='project.task'),
        ),
    ]
