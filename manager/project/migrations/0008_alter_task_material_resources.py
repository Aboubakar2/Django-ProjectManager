# Generated by Django 5.0.1 on 2024-02-12 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_task_softwares_remove_reunion_task_associated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='material_resources',
            field=models.ManyToManyField(blank=True, null=True, to='project.materialresource'),
        ),
    ]
