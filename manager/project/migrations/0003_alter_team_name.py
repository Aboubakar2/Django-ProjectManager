# Generated by Django 5.0.1 on 2024-02-09 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_alter_agent_first_name_alter_agent_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
