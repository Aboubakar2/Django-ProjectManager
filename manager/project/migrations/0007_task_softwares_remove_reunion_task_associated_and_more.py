# Generated by Django 5.0.1 on 2024-02-12 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_alter_materialresource_name_alter_meetingreport_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='softwares',
            field=models.ManyToManyField(related_name='softwares', to='project.software'),
        ),
        migrations.RemoveField(
            model_name='reunion',
            name='task_associated',
        ),
        migrations.AddField(
            model_name='reunion',
            name='task_associated',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.task'),
        ),
    ]
