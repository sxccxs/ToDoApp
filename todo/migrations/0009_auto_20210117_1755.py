# Generated by Django 3.0.8 on 2021-01-17 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0008_auto_20210117_1553'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-created_at'], 'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.RenameField(
            model_name='task',
            old_name='created',
            new_name='created_at',
        ),
    ]