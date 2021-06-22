# Generated by Django 3.1.7 on 2021-06-21 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('section', '0002_remove_section_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='section',
            name='link',
        ),
        migrations.AlterField(
            model_name='section',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
